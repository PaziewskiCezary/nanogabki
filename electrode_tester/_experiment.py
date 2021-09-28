import copy
import datetime
# import logging
import os
import time
import uuid
import warnings
import itertools
import pickle
import decimal
import sys

from pathlib import Path
from typing import Union, Dict, Tuple, List, Iterable
from functools import total_ordering

from tqdm.auto import tqdm

from ._measurement import Measurement
from .devices import BaseDevice
from .common import date_format
from .electrodes import BaseElectrode

@total_ordering
class Experiment():


    def __init__(self,
                *,
                device,
                frequencies: Iterable,
                electrode: BaseElectrode,
                resistances: Tuple[str, str], # Ohm
                channels: Dict[str, int]=None,
                voltage: float=1,
                sampling_rate: int=1024,
                sampling_time: float=5, # seconds
                delay: int=0, # seconds
                tries: int=1,
                results_path: Union[str, Path]='results',
                save_name: Union[str, Path]='',
                scope_range = 2,
                comment: str='',
                ):

        self._uuid = str(uuid.uuid4())
        self._date = time.time()

        self._device = device
        self._resistances = self._prase_resistances(resistances)
        
        self.electrode = electrode
        self.voltage = voltage
        self.sampling_rate = sampling_rate
        self.sampling_time = sampling_time
        self.delay = delay
        self.tries = tries
        self.comment = comment

        self._measurements = []

        self._channels = {
            'ch1' : 0,
            'ch2' : 1,
            'ch3' : 3,
            'gen' : 0,
            }

        if channels:
            for key, val in channels.items():
                self.set_channel(key, val)

        self._frequencies = self._parse_frequencies(frequencies)

        self.results_path = results_path
        self.save_name = save_name

        self.device.set_scope(frequency=sampling_rate, scope_range=scope_range,
                              record_time=sampling_time)
        self.__working_dir = self.results_path
        self.save()
        print(f'starting experiment: "{self.save_path.absolute()}"')

    def __iter__(self) -> 'Experiment':
        self.__iter_measurements = iter(self._measurements)
        return self

    def __next__(self) -> Measurement:
        measurement = Measurement.load(self.__working_dir / self.folder_path.name / next(self.__iter_measurements), working_dir=self.__working_dir / self.folder_path.name)
        return measurement

    def __getitem__(self, index) -> List[Measurement]:
        try:
            measurements = self._measurements[index]
        except IndexError:
            raise IndexError('"index" must be between 0 and number of measurements')
        if isinstance(measurements, str):
            return Measurement.load(self.__working_dir / self.folder_path.name / measurements, working_dir=self.__working_dir / self.folder_path.name)
        return [Measurement.load(self.__working_dir / self.folder_path.name / m, working_dir=self.__working_dir / self.folder_path.name) for m in measurements]
    
    def __repr__(self) -> str:
        """
        return string representation of the object
        """
        tries = f'{len(self)}' + (f'/{self.tries}' if self.tries else '')
        return f'''Experiment(date={self.date},
    electrode: {self.electrode},
    tries: {tries},
    frequencies: {' ,'.join(str(f) for f in self.frequencies)} Hz,
    voltage: {self.voltage} V,
    sampling rate: {self.sampling_rate} Hz,
    sampling time: {self.sampling_time} s''' + (f''',
    comment: {self.comment}''' if self.comment else '') + '\n)'
    
    def __str__(self) -> str:
        """
        return string representation of the object
        """
        return self.__repr__()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Experiment):
            raise ValueError('Can only compare with other "Experiment" class')
        return self._date == other._date

    def __lt__(self, other) -> bool:
        if not isinstance(other, Experiment):
            raise ValueError('Can only compare with other "Experiment" class')
        return self._date < other._date

    def __hash__(self) -> int:
        return hash(self.uuid)

    def __enter__(self) -> Measurement:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.save(overwrite=True)

    def __len__(self) -> int:
        return len(self._measurements)

    def __bool__(self) -> bool:
        return bool(self._measurements)

    def __length_hint__(self):
        return len(self)

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def device(self) -> BaseDevice:
        return self._device
        
    @device.setter
    def device(self, device):
        raise NotImplemented
        if not isinstance(BaseDevice):
            raise ValueError('"device" must be `BaseDevice` type')
        self._device = device

    @property
    def resistances(self) -> Tuple[float, float]:
        return self._resistances

    @resistances.setter
    def resistances(self, resistances:Tuple[float, float]):
        self._resistances = self._prase_resistances(resistances)

    @classmethod
    def _prase_resistances(cls, resistances:Tuple[str, str]) -> tuple:

        if not len(resistances) == 2:
            raise ValueError('"resistances" must be Iterable of lenght 2')

        if any(not isinstance(r, str) for r in resistances):
            raise ValueError('"resistances" must be type "string"')
        try:
            resistances = tuple(decimal.Decimal(resistance) for resistance in resistances)
        except decimal.InvalidOperation:
            raise ValueError('At least one of resistances indices is not convertable to "Decimal"')

        if any(r < 0 for r in resistances):
            raise ValueError('At least one of resistances indices is not none negative integer')

        return resistances

    @property
    def r1(self) -> float:
        r, _ = self.resistances
        return float(r)

    @property
    def r2(self) -> float:
        _, r = self.resistances
        return float(r)

    @property
    def electrode(self) -> BaseElectrode:
        return self._electrode

    @electrode.setter
    def electrode(self, electrode: BaseElectrode):
        if not isinstance(electrode, BaseElectrode):
            raise ValueError(f'"electrode" should be BaseElectrode not "{type(electrode)}"')
        self._electrode = electrode

    @property
    def voltage(self) -> float:
        return self._voltage

    @voltage.setter
    def voltage(self, voltage:float):
        if not isinstance(voltage, (float, int)) or voltage <= 0:
            raise ValueError(f'"voltage" should be positive number not "{voltage}"')
        self._voltage = float(voltage)

    @property
    def sampling_rate(self) -> int:
        return self._sampling_rate

    @sampling_rate.setter
    def sampling_rate(self, sampling_rate:int):
        if not isinstance(sampling_rate, (int)) or sampling_rate <= 0:
            raise ValueError(f'"sampling rate" should be positive integer, not "{sampling_rate}"')
        self._sampling_rate = sampling_rate

    @property
    def fs(self) -> int:
        return self.sampling_rate

    @fs.setter
    def fs(self, fs:int):
        self.sampling_rate = fs

    @property
    def sampling_time(self) -> float:
        return float(self._sampling_time)

    @sampling_time.setter
    def sampling_time(self, sampling_time:float):
        if not isinstance(sampling_time, (int)) or sampling_time <= 0:
            raise ValueError(f'"sampling time" should be positive float, not "{sampling_time}"')
        self._sampling_time = sampling_time

    @property
    def delay(self) -> int:
        return self._delay

    @delay.setter
    def delay(self, delay:int):
        if not isinstance(delay, (int)) or delay < 0:
            raise ValueError(f'"delay" should be non negative integer, not "{delay}"')
        self._delay = delay

    @property
    def tries(self) -> int:
        return self._tries

    @tries.setter
    def tries(self, tries:Union[None, int]):
        if tries is None:
            self._tries = tries
            return
        if not isinstance(tries, (int)) or tries < 0:
            raise ValueError(f'"tries" should be non negative integer, not "{tries}"')
        self._tries = tries

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, comment:str):
        if not isinstance(comment, str):
            raise ValueError(f'"comment" should be string, not "{comment}"')
        self._comment = comment

    @property
    def scope_range(self) -> float:
        return self._scope_range

    @scope_range.setter
    def scope_range(self, value:Union[float, int]):
        if not isinstance(value, (float, int)) or value < 0:
            raise ValueError(f'"scope_range" should be non negative integer or '\
                             f'float, not "{value}"')
        self._scope_range = float(value)

    @property
    def date(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self._date).strftime(date_format)

    @property
    def channels(self) -> Dict[str, int]:
        return copy.copy(self._channels)

    @channels.setter
    def channels(self, channels: Dict[str, int]):
        old_channels = copy.copy(self._channels)

        for key, value in channels.items():
            try:
                self.set_channel(key, value)
            except ValueError:
                self._channels = old_channels
                raise ValueError(f'cannot set "{key}:{value}"')

    def set_channel(self, channel:str, value:int):
        if not channel in self.channels:
            valid_channels_str = '", "'. join(self.channels.keys())
            raise ValueError(f'"{channel}" is not valid channel name, should be one '\
                             f'of "{valid_channels_str}"')
        if not isinstance(value, int) or value < 0:
            raise ValueError(f'"{value}" is not valid parameter, should be non negative int')
        self._channels[channel] = value

    @property
    def frequencies(self) -> Tuple[Union[int, float]]:
        return copy.deepcopy(self._frequencies)

    @frequencies.setter
    def frequencies(self, frequencies:Iterable):
        self._frequencies = self._parse_frequencies(frequencies)

    @classmethod
    def _parse_frequencies(cls, frequencies: Iterable[Union[int, float]]):
        if any(not isinstance(f, (int, float)) for f in frequencies):
            raise ValueError('At least one of channel indices is not of "int" or "float" type')
        if any(f <= 0 for f in frequencies):
            raise ValueError('At least one of channel indices is not none negative "integer" '\
                             'or "float"')

        return tuple(frequencies)

    @property
    def results_path(self) -> Path:
        return self._results_path

    @results_path.setter
    def results_path(self, path:Union[str, Path]):
        if not isinstance(path, (str, Path)):
            raise ValueError('"path" is not of "str" or "pathlib.Path" type')
        p = Path(path)
        if p.exists():
            if p.is_file():
                raise ValueError(f'"{path} exists and is file, not a folder')
        else:
            p.mkdir()
            print(f'created "{path}" folder')

        self._results_path = p

    @property
    def save_name(self) -> Path:
        return self._save_name

    @save_name.setter
    def save_name(self, name:Union[str, Path]):
        if not isinstance(name, (str, Path)):
            raise ValueError('"name" is not of "str" or "pathlib.Path" type')
        
        name = name if name else self.date  
        name = Path(str(name))
        name = name.with_suffix('.exp')
        path =  Path(self.results_path) / name

        if path.exists():
            if path.is_file():
                raise ValueError(f'"{path} already exists')

        self._save_name = name
    
    @property
    def save_path(self) -> Path:
        return Path(self.results_path) / self.save_name
    
    @property
    def folder_path(self) -> Path:
        return self.save_path.with_suffix('')
      
    def start(self, save=True) -> None:

        if not self.device:
            raise Exception('Can\'t run loaded "Experiment"')

        done = False
        finished = False
    
        progress = tqdm(total=self.tries, unit=' measurement')
        for i in itertools.count():

            if not done:
                try:
                    progress.desc = 'taking measurement'
                    progress.refresh()
                    measurement = Measurement(self)
                    measurement.make_measurement(self.device, progress=progress)
                    measurement_save_path = measurement.save(overwrite=True)
                    self._measurements.append(measurement_save_path.name)
                    if save:
                        self.save(overwrite=True)
                    progress.update()
                    progress.refresh()
                    
                    if self.tries and self.tries == i + 1:
                        done = True
                        finished = True
                        progress.desc = 'done'
                        progress.refresh()
                except KeyboardInterrupt:
                    wanring = f'Przerwano pomiar numer {i + 1}, pomiar niezapisany'
                    warnings.warn(wanring)
                    done = True
                
                if not done:
                    try:
                        sleep_time_left = self.delay
                        while sleep_time_left:
                            progress.desc = f'wating {sleep_time_left}s'
                            progress.refresh()
                            time.sleep(1)
                            sleep_time_left -= 1
                    except KeyboardInterrupt:
                        wanring = f'Zakończono na pomiarze numer {i + 1}'
                        warnings.warn(wanring)
                        done = True
            else:
                break

        progress.close()
        return self.save_path.absolute(), finished

    def save(self, overwrite=False) -> None:
        """
        save data to pickle file with exp extension
        """
        
        if self.save_path.exists and self.save_path.is_file():
            if not overwrite:
                raise OSError(f'File "{self.save_path} already exists')

        if self.folder_path.exists() and self.folder_path.is_dir():
            if not overwrite:
                raise OSError(f'Folder "{self.folder_path} already exists')
        self.folder_path.mkdir(exist_ok=overwrite)

        with open(self.save_path, "wb") as file:
            device = self.device
            self._device = None
            object_data = copy.copy(self.__dict__)
            pickle.dump(object_data, file)
            self._device = device
        os.sync()
        return self.save_path

    @staticmethod
    def load(path:str) -> 'Experiment':
        """
        :param path: path to the pickle file
        load pickle file with exp extension
        """

        path = Path(path)

        if path.suffix != '.exp':
            raise ValueError('Wrong file extension! Load "exp" file.')

        with open(path, "rb") as file:
            new = Experiment.__new__(Experiment)
            new_data = pickle.load(file)
            new.__dict__ = new_data
            new.__working_dir = path.parent

        return new
