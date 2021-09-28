from abc import ABC, abstractmethod
from typing import Dict
from collections import namedtuple

Params = namedtuple('Params', ['amplitude', 'amplitude_error', 'phase', 'phase_error', 'offset', 'offset_error', 'frequency', 'frequency_error', 'function'])

class BaseEstimator(ABC):

    @abstractmethod
    def estimate(self, x, y, **kwargs) -> Params:
        ...

