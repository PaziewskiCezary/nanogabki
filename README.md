# Electrode Tester

Foobar is a Python library for testing EEG electrodes.

<!--
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Electrode Tester.

```bash
pip install electrode_tester
```
-->
## Usage

```python
from electrode_tester import Experiment
from electrode_tester.device import DummyDevice # use dummy device
from electrode_tester.electrodes import ViledaElectrode 

frequencies = [0.5, 1, 2, 3, 5, 10, 20, 50, 70, 100] # Hz
tries = 3
sampling_rate = 1_000 # Hz
comment = 'This is my first experiment'

electrode = ViledaElectrode(
    salt_type = 'saline',
    salty_value = 0.9,
    
    normal_height= 1.5, # height of sponge before sqeezing 
    squeeze_height = 0.5, # amount of squueze in the same units as normal_height
    height_delta = 0.1 , # uncentainty of sponge height placed in piston 
    normal_height_var = .1, # variance between sponges due to cutting technique
    
    width = .5,
)

results_path = '/tmp'

with Experiment(device=TiePieDevice(),
                frequencies=freqs,
                electrode = electrode,

                resistances=('392.000', '385.000'), # measures resistance of resistors R1 and R2, must be passed as string in Ohm with the same number of significant numbers as it was displayed
                voltage=1.7, # generator voltage in volts
                sampling_rate=sampling_rate, # sampling rate of osciloscope in Hz
                sampling_time=5,  # dutation of one signal in seconds
                delay=0, # delay between measurements in seconds
                tries=tries, # number of measurements to be taken 
                results_path = results_path, # save path
                save_name = '', # use non-default save name
                scope_range = 2, # range of osciloscope
                comment = comment) as e:

    file_name, finnished = e.start()


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
