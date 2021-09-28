import unittest
import time
import types
import decimal

from pathlib import Path
from tempfile import TemporaryDirectory


from electrode_tester import Experiment
from electrode_tester.device import DummyDevice

class ExperimentTest(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = TemporaryDirectory()
        config = types.SimpleNamespace()
        config.frequencies = tuple(range(1, 101))
        config.electrode_type = 'nano'
        config.salt_type = 'n/a'
        config.salty_value = float("nan")
        config.sponge_high = 1.5
        config.squeeze_value = 0
        config.device = DummyDevice()

        config.resistances = "200", "100"
        config.voltage = 1
        config.sampling_rate = 1024
        config.sampling_time = 5
        config.results_path = Path(self.tmp_dir.name)
        self.config = config


        # defaults params
        self.default_device = config.device
        self.default_resistances = (200, 100)
        self.default_channels = {
        'ch1' : 0,
        'ch2' : 1,
        'ch3' : 3,
        'gen' : 0,
        }
        self.default_frequencies = tuple(range(1, 101))
        self.default_voltage = 1
        self.default_sampling_rate = 1024
        self.default_sampling_time= 5
        self.default_delay = 5*60
        self.default_tries = None
        
        # non defaults params
        self.resistances = ("20", "20")
        self.voltage = 2
        self.sampling_rate = 256
        self.sampling_time = 10
        self.delay = 10*60
        self.tries = 20
        self.channels = {
        'ch1' : 3,
        'ch2' : 2,
        'ch3' : 1,
        'gen' : 1,
        }
        self.frequencies = tuple(range(1,101, 10))

        self._start_time = time.time()
        self.e = Experiment(**self.config.__dict__)

    def test_date(self):
        # probably not the right way
        import datetime
        self.assertTrue(self._start_time <= self.e._date <= time.time())

    def test_defaults(self):
        self.assertEqual(self.e.device, self.default_device)
        self.assertEqual(self.e.resistances, tuple(decimal.Decimal(r) for r in self.default_resistances))
        self.assertEqual(self.e.channels, self.default_channels)
        self.assertEqual(self.e.frequencies, self.default_frequencies)
        self.assertEqual(self.e.voltage, self.default_voltage)
        self.assertEqual(self.e.sampling_rate, self.default_sampling_rate)
        self.assertEqual(self.e.sampling_time, self.default_sampling_time)
        self.assertEqual(self.e.delay, self.default_delay)
        self.assertEqual(self.e.tries, self.default_tries)

    def test_if_properties_exists(self):
        e = self.e

        e.device
        e.uuid
        e.date
        e.resistances
        e.voltage
        e.sampling_rate
        e.sampling_time
        e.delay
        e.tries
        e.channels
        e.frequencies

    def test_aliases(self):
        self.assertEqual(self.e.sampling_rate, self.e.fs)

        r1, r2 = self.e.resistances
        self.assertEqual(r1, self.e.r1)
        self.assertEqual(r2, self.e.r2)

    def test_if_setter_works(self):
        "testing setters with correct values"
        import copy

        e = Experiment(**self.config.__dict__)

        e.resistances = self.resistances
        self.assertEqual(e.resistances, tuple(decimal.Decimal(r) for r in  self.resistances))

        e.channels = self.channels
        self.assertEqual(e.channels, self.channels)

        e.frequencies = self.frequencies
        self.assertEqual(e.frequencies, self.frequencies)

        e.voltage = self.voltage
        self.assertEqual(e.voltage, self.voltage)

        e.sampling_rate = self.sampling_rate
        self.assertEqual(e.sampling_rate, self.sampling_rate)

        e.sampling_time = self.sampling_time
        self.assertEqual(e.sampling_time, self.sampling_time)

        e.delay = self.delay
        self.assertEqual(e.delay, self.delay)

        e.tries = self.tries
        self.assertEqual(e.tries, self.tries)
        tries = None
        e.tries = tries
        self.assertEqual(e.tries, tries)


    def test_uuid(self):
        self.assertRegex(
            self.e.uuid,
            '^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$'
            )

    def test_non_default_channels(self):
        channels = {
        'ch1' : 1,
        'ch2' : 2,
        'ch3' : 3,
        'gen' : 1,
        }
        e = Experiment(**self.config.__dict__, channels=channels)
        self.assertEqual(e.channels, channels)

    def test_incorrect_values_setting_channel(self):
        # test negative value
        with self.assertRaises(ValueError) as e:
            key, value = 'cha1', -1
            self.e.set_channel(key, value)

        # test bad values
        values  = [-1, 1., -1., '1']
        key = 'ch1' 
        for value in values:
            with self.assertRaises(ValueError) as e:
                self.e.set_channel(key, value)


        # test bad keys
        keys  = ['ch0', 1, 1.0]
        value = 0
        for key in keys:
            with self.assertRaises(Exception) as e:
                self.e.set_channel(key, value)

    def test_init_arguments(self):
        e = Experiment(
            device = self.config.device,
            resistances = self.resistances,
            voltage = self.voltage,
            sampling_rate = self.sampling_rate,
            sampling_time = self.sampling_time,
            delay = self.delay,
            tries = self.tries,
            channels = self.channels,
            frequencies = self.frequencies,
            )

        self.assertEqual(e.resistances, self.resistances)
        self.assertEqual(e.voltage, self.voltage)
        self.assertEqual(e.sampling_rate, self.sampling_rate)
        self.assertEqual(e.sampling_time, self.sampling_time)
        self.assertEqual(e.delay, self.delay)
        self.assertEqual(e.tries, self.tries)
        self.assertEqual(e.channels, self.channels)
        self.assertEqual(e.frequencies, self.frequencies)

    def test_docstring(self):
        # TODO add properties
        obj = self.e
        for fu in dir(self.e):
            attr = getattr(obj, fu)
            if not hasattr(attr, '__call__'):
                continue
            if fu.startswith('__') and fu.endswith('__'):
                continue
            if not attr.__doc__ or attr.__doc__.strip():
                self.fail(f'No docstring for {obj.__class__.__name__}.{fu}')
                
    def test_repr_str(self):
        print(str(self.e))
        print(repr(self.e))
        

if __name__ == '__main__':
    unittest.main()

