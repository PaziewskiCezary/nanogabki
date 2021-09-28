import numpy as np
import scipy.signal as ss

from ._base_estimator import BaseEstimator, Params

class FitHilbert(BaseEstimator):

    def estimate(self, x, y, **kwargs):
        
        frequency = kwargs.get('frequency')
        if not frequency:
            raise ValueError('"frequency" argument is not passed')

        '''
        :param x: time vector
        :param y: signal vector
        Computes "amplitude" and "phase" by signal demoulation using Hilbert transform and analitical signal
        '''
        
        args = {}
        
        offset = np.mean(y)
        y -= offset
        
        
        hilbert = ss.hilbert(y)
        
        hilbert_abs = np.abs(hilbert)
        hilbert_abs_std = np.std(hilbert_abs)
        hilbert_abs_mean = np.mean(hilbert_abs)
        amplitudes = hilbert_abs[(hilbert_abs < hilbert_abs_mean + hilbert_abs_std) * (hilbert_abs > hilbert_abs_mean - hilbert_abs_std)]
        args['amplitude'] = np.median(amplitudes)
        args['amplitude_error'] = 0.00056
        
        hilbert_phase = np.unwrap(np.angle(hilbert)) - 2 * np.pi * frequency * x + np.pi/2
        hilbert_phase_std = np.std(hilbert_phase)
        hilbert_phase_mean = np.mean(hilbert_phase)
        phases = hilbert_phase[(hilbert_phase < hilbert_phase_mean + hilbert_phase_std) * (hilbert_phase > hilbert_phase_mean - hilbert_phase_std)]   
        phase = np.median(phases)
        phase = ((phase + np.pi) % (2 * np.pi)) - np.pi
        if phase < 0:
            phase += 2*np.pi
        args['phase'] = phase
        args['phase_error'] = 0.00072
        
        args['offset'] = offset
        args['offset_error'] = 0.00024 
        args['frequency'] = None
        args['frequency_error'] = None
        args['function'] = None
        
        params = Params(**args)
        return params
        
        
