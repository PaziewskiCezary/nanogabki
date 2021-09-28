import os
import pickle
import warnings

from typing import Union
from pathlib import Path

import numpy as np

class SignalContainer:

    def __init__(self, data, *, frequency):
        self._data = self._parse_data(data)
        self._frequency = self._parse_frequency(frequency)

    def __iter__(self):
        """
        return iterator object
        """
        self.__iter_n = 0
        return self

    def __next__(self):
        """
        return next item of the data
        """
        if self.__iter_n < 3:
            signal = self.data[self.__iter_n]
            self.__iter_n += 1
            return signal
        raise StopIteration

    def __getitem__(self, index):
        """
        :param index: index of searching measurement   #to chyba nie ma sensu, czym jest number of signals nie powinno być number of channels?
        """
        try:
            return self.data[index]
        except IndexError:
            raise IndexError('"index" must be between 0 and number of signals')

    @property
    def data(self):
        """
        make copy of the data
        """
        return self._data.copy()

    def _parse_data(self, data):
        """
        :param data: data from one measurement
        check format and shape of the data
        """
        if not isinstance(data, np.ndarray):
            try:
                data = np.array(data)
            except Exception:
                raise ValueError('can\'t convert to "np.ndarray"')

        if (len(data.shape) != 2) or (data.shape[0] < 3): 
            raise ValueError(f'data should be shape 3 by n, not {data.shape}')
        if data.shape[0] > 3:
            data = data[:3, :]
            warnings.warn(f'Truncating data to shape 3 by {data.shape[1]}')
        return data

    @property
    def frequency(self):
        """
        get the frequency
        """
        return self._frequency

    def _parse_frequency(self, frequency):
        """
        :param frequency: current frequency
        check the type of frequency
        """
        if not isinstance(frequency, (int, float)) and frequency >= 0:
            raise ValueError(f'frequency mus be "int" or "float" type, not {type(frequency)}')
        return frequency

    def __repr__(self):
        """
        str representation of the class
        """
        return f'SignalContainer(frequency={self.frequency})'
    
    def __str__(self):
        """
        str representation of the class
        """
        return self.__repr__()
    
    @property
    def chan1(self):
        """
        get data from channel 1
        """
        return self._data[0]

    @property
    def chan2(self):
        """
        get data from channel 2
        """
        return self._data[1]

    @property
    def chan3(self):
        """
        get data from channel 3
        """
        return self._data[2]

    @property
    def v1(self):
        """
        get the difference of channel 2 and channel 1
        """
        return self.chan1 - self.chan2

    @property
    def v2(self):
        """
        get the difference of channel 3 and channel 2
        """
        return self.chan2 - self.chan3

    def save(self, path, overwrite=False) -> None:
        """
        saves data to file with mes extension
        """
        path = Path(path)
        if path.exists() and path.is_file():
            if not overwrite:
                raise IOError(f'File "{path}" already exists')

        with open(path, "wb") as file:
            pickle.dump(self, file)
        os.sync()
        return path

    @staticmethod
    def load(path:Union[str, Path]) -> 'SignalContainer':
        """
        :path: path to the load file
        load pickle file with cont extension
        """
        path = Path(path)
        if not path.suffix == '.cont':
            raise ValueError('Wrong file extension! Load "cont" file.')
        with open(path, "rb") as file:
            container = pickle.load(file)
        return container