# Foobar

Foobar is a Python library for testing EEG electrodes.

<!--
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```
-->
## Usage

```python
# import Electrode and Deive
from electrode_tester import Experiment
from electrode_tester.device import DummyDevice

frequencies = [0.5, 1, 2, 3, 5, 10, 20, 50, 70, 100] # Hz
tries = 3
sampling_rate = 1_000 # Hz
comment = 'This is my first experiment'

with Experiment(device=DummyDevice(),
                frequencies=frequencies,
                electrode_type='vileda',
                salt_type='saline',
                salty_value=0.9,
                sponge_high=1.5,
                squeeze_value=1,
                resistances=('400.000', '400.000'), 
                voltage=1.7,
                sampling_rate=sampling_rate,
                sampling_time=5,
                delay=0,
                tries=tries,
                results_path = '/tmp',
                save_name = '',
                scope_range = 2,
                comment = comment) as experiment:

    file_name, finished = experiment.start()


print(experiment)


# view collected data
# iterate over measurements
for measurement in Experiment.load(file_name):
    print(measurement)
    # iterate over frequencies
    for measurement_data in measurement:
        pass

```

## License
<!--
[MIT](https://choosealicense.com/licenses/mit/)
-->