import copy
import datetime
import os
import time
import uuid
import pickle
import decimal

from pathlib import Path
from typing import Tuple, Union, Iterable, List
from functools import total_ordering

import numpy as np

from ._signal_container import SignalContainer
from .common import date_format


@total_ordering
class Measurement():

    def __init__(self, parent):
    
        self.__loaded = False

        self._uuid = str(uuid.uuid4())
        self._date = time.time()
        self._measurements_data = []

        self.frequencies = copy.deepcopy(parent.frequencies)
        self.resistances = copy.deepcopy(parent.resistances)
        self.voltage = copy.copy(parent.voltage)
        self.sampling_rate = copy.copy(parent.sampling_rate)
        self.sampling_time = copy.copy(parent.sampling_time)
        self.parent_folder_path = parent.folder_path
        self.save(overwrite=True)
        self.__working_dir = Path('')

    def __iter__(self) -> 'Measurement':
        """
        return iterator object
        """
        self.__iter_data = iter(self._measurements_data)
        return self

    def __next__(self) -> SignalContainer:
        """
        return next item of the data
        """
        return SignalContainer.load(self.__working_dir / self.folder_path.name / next(self.__iter_data))


    def __getitem__(self, index) -> List[SignalContainer]:
        """
        :param index: index of the searching frequency
        return: measurement for searched frequency
        """
        try:
            containers = self._measurements_data[index]
            if isinstance(containers, str):
                return SignalContainer.load(self.__working_dir / self.folder_path.name / containers)
            return [SignalContainer.load(self.__working_dir / self.folder_path.name / path) for path in containers]
        except IndexError:
            raise IndexError('"index" must be between 0 and length of frequencies')

    def __call__(self, frequency) -> SignalContainer:
        '''
        :param frequency: frequency for which data is searched for
        returns data for first frequency that is found, else rasies ValueError
        '''
        if frequency not in self.frequencies:
            raise ValueError('A given frequency does not exist in this object')
        index = self.frequencies.index(frequency)
        return SignalContainer.load(self.__working_dir / self.folder_path.name / self._measurements_data[index])

    def __repr__(self) -> str:
        """
        return string representation of the object
        """
        date = datetime.datetime.fromtimestamp(self._date).strftime(date_format)
        return f'''Measurement(date={date}
    frequency = {self._sampling_rate} Hz,
    resistances = {', '.join(str(r) for r in self._resistances)} Ohm,
    voltage = {self._voltage} V
    )'''

    def __str__(self) -> str:
        """
        return string representation of the object
        """
        return self.__repr__()

    def __eq__(self, other) -> bool:
        """
        check if data is the same in two measurement files
        """
        if not isinstance(other, Measurement):
            raise ValueError('Can only compare with other "Measurement" class')
        return self._date == other._date

    def __lt__(self, other) -> bool:
        """
        check if data is strictly less than other measurement data
        """
        if not isinstance(other, Measurement):
            raise ValueError('Can only compare with other "Measurement" class')
        return self._date < other._date

    def __hash__(self) -> int:
        """
        return hash of universally unique identifier
        """
        return hash(self.uuid)

    def __len__(self) -> int:
        """
        return length of data matrix -> number of frequencies
        """
        return len(self._measurements_data)

    def __bool__(self) -> bool:
        """
        check if length of data matrix is equal number of frequencies
        """
        return len(self._measurements_data) == len(self.frequencies)

    def __length_hint__(self) -> int:
        """
        return an estimated length for the object
        """
        return len(self)
        
    @property
    def uuid(self) -> str:
        """
        get universally unique identifier
        """
        return self._uuid

    @property
    def resistances(self) -> Tuple[float, float]:
        """
        get the resistances
        """
        return self._resistances

    @resistances.setter
    def resistances(self, resistances:Iterable[Tuple[str, str]]):
        """
        :param resistances: values of resistance
        set the resistances
        """
        if not isinstance(resistances, (list, tuple)):
            raise ValueError('"resistances" must be "list" or "tuple" type')
        if len(resistances) != 2:
            raise ValueError('"resistances" must be length of 2')

        if any(not isinstance(r, decimal.Decimal) for r in resistances):
            raise ValueError('"resistances" must be type "Decimal"')
        self._resistances = tuple(resistances)

    @property
    def r1(self) -> float:
        """
        get the value of first resistor
        """
        r, _ = self.resistances
        return float(r)

    @property
    def r2(self) -> float:
        """
        get the value of second resistor
        """
        _, r = self.resistances
        return float(r)

    @property
    def voltage(self) -> float:
        """
        get the value of voltage
        """
        return self._voltage

    @voltage.setter
    def voltage(self, voltage:Union[float, int]):
        """
        :param voltage: voltage of generator
        set the voltage of generator
        """
        if not isinstance(voltage, (float, int)):
            raise ValueError('"voltage" must be "float" or "int" type')
        if not voltage > 0:
            raise ValueError('"voltage" must grater than 0')
        self._voltage = float(voltage)

    @property
    def sampling_rate(self) -> int:
        """
        get the sampling rate
        """
        return self._sampling_rate

    @sampling_rate.setter
    def sampling_rate(self, rate:int):
        """
        :param rate: sampling rate 
        set the sampling rate of measurement
        """
        if not isinstance(rate, int):
            raise ValueError('"sampling_rate" must be "int" type')
        if not rate > 0:
            raise ValueError('"sampling_rate" must grater than 0')
        self._sampling_rate = rate

    @property
    def fs(self) -> int:
        '''alias for sampling_rate'''
        return self.sampling_rate

    @fs.setter
    def fs(self, rate:int):
        """
        :param rate: sampling rate 
        set the sampling rate of measurement
        """
        self.sampling_rate = rate

    @property
    def frequencies(self) -> Tuple[int]:
        """
        get the frequencies
        """
        return copy.deepcopy(self._frequencies)

    @frequencies.setter
    def frequencies(self, frequencies:Iterable[Union[float, int]]):
        """
        :param frequencies: list of frequencies for which the measurements will be made
        set the frequencies for the experiment
        """
        if not isinstance(frequencies, (list, tuple)):
            raise ValueError('"frequencies" must be "list" or "tuple" type')
        self._frequencies = tuple(frequencies)

    @property
    def sampling_time(self) -> float:
        """
        get number of seconds of one measurement for one frequency
        """
        return self._sampling_time

    @sampling_time.setter
    def sampling_time(self, time_value:Union[float, int]):
        """
        :param time_value: number of seconds of one measurement for one frequency
        set number of second
        """
        if not isinstance(time_value, (float, int)):
            raise ValueError('"sampling_time" must be "float" or int" type')
        if not time_value > 0:
            raise ValueError('"sampling_time" must grater than 0')
        self._sampling_time = float(time_value)

    @property
    def measurements_data(self) -> List[SignalContainer]:
        """
        return copy of data
        """
        return list(iter(self))

    @property
    def date(self) -> str:
        """
        return current date 
        """
        return datetime.datetime.fromtimestamp(self._date).strftime(date_format)

    @property
    def time_vector(self) -> np.ndarray:
        """
        return vector with time samples 
        """
        return np.linspace(0,
                           self.sampling_time,
                           int(self.sampling_rate * self.sampling_time),
                           endpoint=True)

    @property
    def parent_folder_path(self) -> Path:
        return self._parent_folder_path

    @parent_folder_path.setter
    def parent_folder_path(self, path):

        if not isinstance(path, Path):
            raise ValueError('"path" must be "Path" type')
        self._parent_folder_path = path

    @property
    def save_path(self) -> Path:
        return self.parent_folder_path / Path(f'{self.date}.mes')

    @property
    def folder_path(self) -> Path:
        return self.save_path.with_suffix('')
    
    def save(self, overwrite=False) -> None:
        """
        saves data to file with mes extension
        """
        if self.save_path.exists() and self.save_path.is_file():
            if not overwrite:
                raise IOError(f'File "{self.save_path}" already exists')
                
        if self.folder_path and self.folder_path.is_dir():
            if not overwrite:
                raise IOError(f'Folder "{self.folder_path}" already exists')
        self.folder_path.mkdir(exist_ok=overwrite)

        with open(self.save_path, "wb") as file:
            object_data = self.__dict__
            object_data['parent'] = ''
            pickle.dump(object_data, file)
        os.sync()
        return self.save_path

    @staticmethod
    def load(path:Union[str, Path], working_dir:Union[str, Path]='') -> 'Measurement':
        """
        :path: path to the load file
        load pickle file with mes extension
        """
        
        path = Path(path) 
       
        if not path.suffix == '.mes':
            raise ValueError('Wrong file extension! Load "mes" file.')
        with open(path, "rb") as file:
            new = Measurement.__new__(Measurement)
            new_data = pickle.load(file)
            new.__dict__ = new_data
            new.__loaded = True
            new.__working_dir = Path(working_dir)

        return new

    def make_measurement(self, device, *, progress=None, save=True) -> None:
        """
        :param device: object with device class
        :param progress: information about progress of experiment
        :param save: if save measurement file
        make measurement for every given frequency
        """
        if self.__loaded:
            raise Exception('Can\'t use it on loaded "measurement"')
        total = len(self.frequencies)
        for i, frequency in enumerate(self.frequencies):
            if progress is not None:
                progress.desc = f'{i+1}/{total} freq={frequency}Hz'
                progress.refresh()
            device.set_generator(frequency=frequency, amplitude=self.voltage)
            measurement_data = device.get_data()
            measurement_data = measurement_data[:3]
            container = SignalContainer(measurement_data, frequency=frequency)
            container_path = self.folder_path / f'{i}_container.cont'
            container_path = container.save(container_path)
            self._measurements_data.append(container_path.name)
        if save:
            self.save(overwrite=True)
