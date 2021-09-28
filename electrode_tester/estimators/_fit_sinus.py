import numpy as np
import scipy.optimize

from functools import partial
from ._base_estimator import BaseEstimator, Params

class FitSinus(BaseEstimator):

    def estimate(self, x, y, **kwargs):        
        '''
        :param x: time vector
        :param y: signal vector
        Computes sinal paramitest by fitting sinus funtion
        '''
        frequency = kwargs.get('frequency')
        if not frequency:
            raise ValueError('"frequency" argument is not passed')
        '''Fits sin to the input time sequence, and return fitting parameters tuple `Params"'''

        x = np.array(x)
        y = np.array(y)

        guess_amplitude = np.std(y) * 2.**0.5
        guess_offset = np.mean(y)
        guess_frequency = frequency
        guess = np.array([guess_amplitude, 0., guess_offset, guess_frequency])

        def sinfunc(t, A, p, c, f):  return A * np.sin(2*np.pi * f *t + p) + c

        popt, pcov = scipy.optimize.curve_fit(sinfunc, x, y, p0=guess, maxfev = 10000)
        A, p, c, f = popt
        if A < 0:
            params = self.estimate(x, -(y-c)+c, **kwargs)
            y = -(y-c)+c
            popt, pcov = scipy.optimize.curve_fit(sinfunc, x, y, p0=guess, maxfev = 10000)
            A, p, c, f = popt
            p = p - np.pi
        p = (p + 2 * np.pi ) % (2 * np.pi)
        
        popt = A, p, c, f
        function = partial(sinfunc, A=A,p=p,c=c, f=f)
        
        args = {}
        names = ['amplitude', 'phase', 'offset', 'frequency']
        for val, val_error, name in zip(popt, np.diag(pcov), names):
            args[name] = val
            args[name+'_error'] = val_error
        args['function'] = function

        params = Params(**args)
        return params
