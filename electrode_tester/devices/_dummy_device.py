import types

import numpy as np

from ._base_device import BaseDevice

class DummyDevice(BaseDevice):
    def __init__(self):
        self.gen = types.SimpleNamespace()
        self.scp = types.SimpleNamespace()

        self.set_generator()
        self.start_generator()
        self.set_scope()

        self.__name = 'dummy device'

    @property
    def name(self) -> str:
        return self.__name

    def get_data(self) -> np.ndarray:
        time = np.linspace(0, self.record_time, self.len_sig, endpoint=True)
        data = self.amplitude * np.sin(2 * np.pi * self.gen_freq * time)
        data = np.stack((data, 2 / 3. * data, 1 / 3. * data, data))
        data = data + self.amplitude / 10 * np.random.random(data.shape)
        return data

    def set_generator(self, *, frequency=1, amplitude=0.1, offset=0,
                            signal_type='SINE') -> None:

        self.gen_freq = frequency
        self.amplitude = amplitude
        self.offset = offset

    def start_generator(self) -> None:
        pass

    def stop_generator(self) -> None:
        pass

    def set_scope(self, *, frequency=1024, scope_range=0.2, record_time=3) -> None:
        self.scope_freq = frequency
        self.record_time = record_time
        self.len_sig = int(frequency * record_time)


