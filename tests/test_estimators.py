import numpy as np

from collections import defaultdict

Path = 

from _fit_function import FitSinus
from _fit_hilbert import FitHilbert
from _fit_fourier import FitFourier
from tqdm import tqdm

import concurrent.futures

TEST_N = 1_000_00
#TEST_N = 1_000_00

possible_relative_error = 10**(-2)

ranges = {
    'amplitude': (0, 1000),
    'phase': (0, 2 * np.pi),
    'offset': (-1000, 1000),
#     'offset': (0, 0),
    'frequency': (1, 110),
    'noise': (0, 1000),
    'fs': (512, 5000),
    't': (3, 15)
}


def generate_sine(*, amplitude, frequency, phase, offset, noise, fs, t):
    x = np.arange(0, t, 1/fs)
    y = amplitude * np.sin(x * 2 * np.pi * frequency + phase) + offset + noise * (2 * np.random.random(x.size) - 1)
    return x, y


passed = True
failed = 0
failed_params_counter = defaultdict(int)
ans_all = defaultdict(list)
print_errors = []

def make_test(estimator, params):
    t, signal = generate_sine(**params)
    params_fitted = estimator.estimate(t, signal, **params)

    to_print = ''
    failed_params = defaultdict(None)
    ans = defaultdict(None)

    for key in ['amplitude', 'phase', 'offset', 'frequency']:
        try:
            if not getattr(params_fitted, key):
                continue
            true_error = params[key] - getattr(params_fitted, key)
            reltive_error =  np.abs(true_error) / abs(params[key])
            ans[key] = reltive_error
            
            if reltive_error > possible_relative_error:
                to_print +=(f'{key}: actucal: {params[key]}, fitted: {getattr(params_fitted, key)}, error: {true_error:<5}, relative: {reltive_error:<5}\n')
                failed_params[key] = (params[key], getattr(params_fitted, key))
                
            
        except:
            ans[key] = None
            failed_params[key] = None
    if to_print:
        to_print += str(params)
        to_print += '\n'

    return ans, failed_params, to_print

def make_params(ranges, noise=0.05):
    params = {}
    params['amplitude'] = np.random.uniform(*ranges['amplitude'])
    params['phase'] = np.random.uniform(*ranges['phase'])
    params['offset'] = np.random.uniform(*ranges['offset'])
    params['frequency'] = int(np.random.uniform(*ranges['frequency']))
    params['noise'] = np.random.uniform(ranges['noise'][0], noise * params['amplitude'])
    params['fs'] = int(np.random.uniform(*ranges['fs']))
    params['t'] = int(np.random.uniform(*ranges['t']))
    return params

try:
    estimator = FitHilbert()
    params_list = [make_params(ranges) for _ in range(TEST_N)]
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(make_test, estimator, params) for params in params_list]
        for result in tqdm(concurrent.futures.as_completed(results), total=TEST_N, mininterval=1, maxinterval=2):
            ans, failed_params, to_print = result.result()
            if to_print:
                failed += 1
                print_errors.append(to_print)

            for key, val in failed_params.items():
                if val:
                    failed_params_counter[key] += 1

            for key, val in ans.items():
                if val:
                    ans_all[key].append(val)
except KeyboardInterrupt:
    exit(1)


if failed:
    for i, error in enumerate(print_errors):
        print(i, error)
    print(f'failed {failed} from {TEST_N} which is {failed/TEST_N * 100:2}%')
    print(failed_params_counter)
else:
    print(f'All {TEST_N} tests passed')


for key, val in ans_all.items():
    print(f'"{key}" relative error:\tmean={np.mean(val):<18f}\tstd={np.std(val):<18f}')
