import types

from abc import ABC, abstractmethod

import numpy as np


class BaseDevice(ABC):
    gen: types.SimpleNamespace()
    scp: types.SimpleNamespace()

    __name: str

    @abstractmethod
    def get_data(self) -> np.ndarray:
        ...

    @abstractmethod
    def set_generator(self, *, frequency=1, amplitude=0.1, offset=0,
                            signal_type='SINE') -> None:
        ...

    @abstractmethod
    def start_generator(self) -> None:
        ...

    @abstractmethod
    def stop_generator(self) -> None:
        ...

    @abstractmethod
    def set_scope(self, *, frequency=1024, scope_range=0.2, record_time=3) -> None:
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        return self.__name

