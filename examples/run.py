from electrode_tester import Experiment
from electrode_tester.devices import TiePieDevice
from electrode_tester.electrodes import ViledaElectrode

freqs = list(range(1, 101, 1))
tries = 15
sampling_rate = 1_000
comment = ''

electrode = ViledaElectrode(
    salt_type = 'saline',
    salty_value = 0.9,
    
    normal_height= 1.5, # height of sponge before sqeezing 
    squeeze_height = 0.5, # amount of squueze in the same units as normal_height
    height_delta = 0.1 , # uncentainty of sponge height placed in piston 
    normal_height_var = .1, # variance between sponges due to cutting technique
    
    width = .5,
)

results_path = '/home/USER/results'

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
