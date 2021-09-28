from ._base_estimator import BaseEstimator, Params
import numpy as np

class FitFourier(BaseEstimator):
    
    def __search_min(self, A, value):
        B = np.abs(A - value)
        idx = np.argwhere(B == np.min(B))[0][0]
        return idx

    def estimate(self, x, y, **kwargs):
        frequency = kwargs.get('frequency')
        Fs = kwargs.get('fs')
        if not Fs:
            raise ValueError('"fs" argument is not passed')
        if not frequency:
            raise ValueError('"frequency" argument is not passed')
    
        S = np.fft.rfft(y) / len(y)
        S[1:] *= 2
        F = np.fft.rfftfreq(len(y), 1/Fs)

        args = {}
        
        idx_offset = self.__search_min(F, 0)
        args['offset'] = np.abs(S[idx_offset]) * np.sign(np.real(S[idx_offset]))
        args['offset_error'] = 0.00024
        
        idx_freq = self.__search_min(F, frequency)
        args['amplitude'] = np.abs(S[idx_freq])
        args['amplitude_error'] = 0.00033
        
        phase = np.angle(S[idx_freq]) + np.pi / 2
        if phase < 0:
            phase += np.pi * 2
        args['phase'] = phase
        args['phase_error'] = 0.00052
        
        args['function'] = None
        
        args['frequency_error'] = None
        args['frequency'] = None
        
        params = Params(**args)
        return params
