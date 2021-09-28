from collections import defaultdict
from datetime import timedelta
from .utils import resistance_measuerment_error, limit_measurements
from .estimators import FitSinus, BaseEstimator, FitFourier

class ExperimentAnalysis():
    __default_estimator = FitSinus()
        
    def analyze(self, experiment, *, time_limit: timedelta=timedelta(hours=24), 
                                     estimator=None, calculate_parameters=None, estimator_params={}):

        
        if not estimator:
            estimator = ExperimentAnalysis.__default_estimator
        self.estimator = estimator
        
        self.experiment = experiment
        self.electrode = experiment.electrode
        self.estimator_params = estimator_params

        self.resistances = defaultdict(list)
        self.resistances_errors = defaultdict(list)

        self.resistivities = defaultdict(list)
        self.resistivites_error = defaultdict(list)

        if not estimator:
            estimator = ExperimentAnalysis.__default_estimator
        self.estimator = estimator
        
        measurement_analysiator = MeasurementAnalysis()
        time_deltas = []
        for time_delta, measurement in limit_measurements(self.experiment, time_limit):
            time_deltas.append(time_delta)
            results = measurement_analysiator.analyze(measurement, electrode=self.experiment.electrode, estimator=self.estimator, calculate_parameters=calculate_parameters, estimator_params=estimator_params)
            if calculate_parameters is None or 'resistance' in calculate_parameters:
                resistances, resistances_errors = results['resistance']
                for key, val in zip(measurement.frequencies, resistances):
                    self.resistances[key].append(val)
                for key, val in zip(measurement.frequencies, resistances_errors):
                    self.resistances_errors[key].append(val)

            if calculate_parameters is None or 'resistivity' in calculate_parameters:              
                resistivities, resistivites_error = results['resistivity']
                
                for key, val in zip(measurement.frequencies, resistivities):
                    self.resistivities[key].append(val)
                for key, val in zip(measurement.frequencies, resistivites_error):
                    self.resistivites_error[key].append(val) 

        results = dict()
        if calculate_parameters is None or 'resistance' in calculate_parameters:
            results['resistance'] = (self.resistances, self.resistances_errors)

        if calculate_parameters is None or 'resistivity' in calculate_parameters:
            results['resistivity'] = (self.resistivities, self.resistivites_error)

        return time_deltas, results
        

class MeasurementAnalysis():
    __default_estimator = FitSinus()
    

    def _calc_resistances(self):

        resistances, errors = [] , []
        
        for frequency_signal_container in self.measurement:
        
            Vr1_fit = self.estimator.estimate(x=self.measurement.time_vector,
                                     y=frequency_signal_container.v1, 
                                     frequency=frequency_signal_container.frequency,
                                     **self.estimator_params
                                    )
            R1 = self.measurement.r1
            Vg_fit = self.estimator.estimate(x=self.measurement.time_vector,
                                    y=frequency_signal_container.v2, 
                                    frequency=frequency_signal_container.frequency,
                                    **self.estimator_params
                                   )
            
            
            
            Rg = Vg_fit.amplitude * R1 / Vr1_fit.amplitude
            error = self._resistance_error(Vg_fit, Vr1_fit, R1)
            
            resistances.append(Rg)
            errors.append(error)
        return resistances, errors
    

    def _resistance_error(self, Vg_fit, Vr1_fit, R1):
        
        Vg = Vg_fit.amplitude
        Vr1 = Vr1_fit.amplitude
        
        uVg = Vg_fit.amplitude_error
        uVr1 = Vr1_fit.amplitude_error
        uR1 = resistance_measuerment_error(R1) / 3**.5
        
        Vg_derivative = R1 * uVg / Vr1
        R1_derivative = Vg * uR1 / Vr1
        Vr1_derivative = Vg * R1 * uVr1 / (Vr1)**2
        
        urg = (Vg_derivative**2 + R1_derivative**2 + Vr1_derivative**2)**.5
        return urg
    

    def _calc_resistivities(self):
        
        resistivities, resistivites_error = [], []
        
        resistances, errors, *_ = (self.resistances, self.resistances_errors) if self.resistances else self._calc_resistances()
        
        for resistance, resistance_error in zip(resistances, errors):
            resistivity = resistance * self.electrode.width**2 / (self.electrode.height)
            resistivity_error = self._resistivitis_errors(resistance, resistance_error)
            
            resistivities.append(resistivity)
            resistivites_error.append(resistivity_error)
        
        return resistivities, resistivites_error
        
        

    def _resistivitis_errors(self, resistance, resistance_error):

        rg_derivative = self.electrode.width**2 * resistance_error / self.electrode.height
        h_derivative = resistance * self.electrode.width**2 * self.electrode.height_error / (self.electrode.height*2)
        
        uro = (rg_derivative**2 + h_derivative**2)**.5
        
        return uro
        
   

    def analyze(self, measurement, *, electrode, estimator=None, calculate_parameters=None, estimator_params={}):

        self.measurement = measurement
        self.electrode = electrode
        self.estimator_params = estimator_params

        self.resistances = None
        self.resistances_errors = None

        self.resistivities = None
        self.resistivites_error = None

        if not estimator:
            estimator = MeasurementAnalysis.__default_estimator
        self.estimator = estimator
            
        results = dict()
        if calculate_parameters is None or 'resistance' in calculate_parameters:
            resistances, resistances_errors = self._calc_resistances()
            results['resistance'] = resistances, resistances_errors
        
            self.resistances = resistances
            self.resistances_errors = resistances_errors


        if calculate_parameters is None or 'resistivity' in calculate_parameters:
            resistances_with_errors = [resistances, resistances_errors] if 'resistance' in results else None
            resistivities, resistivites_error = self._calc_resistivities()
            results['resistivity'] = resistivities, resistivites_error

        return results
