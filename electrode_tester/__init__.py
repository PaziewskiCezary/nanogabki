"""
electrode_tester

A Python module helping with automatization of testing characterization of EEG electrodes.
"""

__version__ = '0.9.3'
__author__ = 'Cezary Paziewski'

__maintainers__ = [
    'Cezary Paziewski',
    'Ada Kochlewska',
    'Martyna Poziomska',
]
import sys as _sys

if not (_sys.version_info.major == 3 and _sys.version_info.minor >= 9):
    _sys.exit("Use python 3.9+")

from ._experiment import Experiment
from ._analysis import MeasurementAnalysis, ExperimentAnalysis

from . import electrodes
from . import devices
from . import estimators

from . import common
from . import utils



