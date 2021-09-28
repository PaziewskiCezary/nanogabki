import unittest
import types

from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

from electrode_tester._measurement import Measurement
from electrode_tester.device import DummyDevice


class MeasurementTest(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.tmp_dir = TemporaryDirectory()
        parent = types.SimpleNamespace()
        parent.frequencies = tuple(range(1, 101, 5))
        parent.resistances = 200, 100
        parent.voltage = 1.7
        parent.sampling_rate = 256
        parent.sampling_time = 5*60
        parent.results_path = Path(self.tmp_dir.name)
        self.parent = parent
        self.measurement = Measurement(parent)

    def make_measurement(self, measurement):
        device = DummyDevice()

        with redirect_stdout(None):
            measurement.make_measurement(device)

    @classmethod
    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_step01_creating(self):
        self.measurement = Measurement(self.parent)

    def test_step02_making_measurements(self):
        self.make_measurement(self.measurement)

    def test_step03_iter(self):
        self.make_measurement(self.measurement)

        for _ in self.measurement:
            ...

    def test_step04_indexing(self):
        self.make_measurement(self.measurement)


        self.measurement[0]
        self.measurement[:]

    def test_step05_str(self):
        str(self.measurement)

    def test_step06_repr(self):
        repr(self.measurement)

    def test_step07_less_operator(self):
        measurement = Measurement(self.parent)
        self.assertTrue(self.measurement < measurement)

    def test_step08_grater_operator(self):
        measurement = Measurement(self.parent)
        self.assertFalse(self.measurement > measurement)

    def test_step09_equal_operator(self):
        measurement = Measurement(self.parent)
        self.assertTrue(self.measurement == self.measurement)

    def test_step11_hash(self):
        hash(self.measurement)

    def test_step12_bool(self):
        bool(self.measurement)

    def test_step13_hint_lenth(self):
        self.make_measurement(self.measurement)

        self.assertEqual(len(self.measurement), len(self.parent.frequencies))

    def test_step14_hint_lenth(self):
        self.make_measurement(self.measurement)

        self.assertEqual(self.measurement.__length_hint__(), len(self.parent.frequencies))

    def test_step15_uuid(self):
        self.measurement.uuid


    def test_step16_resistances_getter(self):
        self.measurement.resistances

    def test_step17_resistances_setter(self):
        self.measurement.resistances = [200, 100]

    def test_step18_resistances_setter_with_invalid_values(self):
        with self.assertRaises(ValueError):
            self.measurement.resistances = ["200", None]

    def test_step19_voltage_getter(self):
        self.measurement.voltage

    def test_step20_voltage_setter(self):
        self.measurement.voltage = 1.7

    def test_step21_voltage_setter_with_invalid_values(self):
        with self.assertRaises(ValueError):
            self.measurement.voltage = "1.7"


    def test_step22_sampling_rate_getter(self):
        self.measurement.sampling_rate

    def test_step23_sampling_rate_setter(self):
        self.measurement.sampling_rate = 1024

    def test_step24_sampling_rate_setter_with_invalid_values(self):
        with self.assertRaises(ValueError):
            self.measurement.sampling_rate = "1.7"


    def test_step25_fs_getter(self):
        self.measurement.fs

    def test_step26_fs_setter(self):
        self.measurement.fs = 1024

    def test_step27_fs_setter_with_invalid_values(self):
        with self.assertRaises(ValueError):
            self.measurement.fs = "1.7"


    def test_step28_frequencies_getter(self):
        self.measurement.frequencies

    def test_step29_frequencies_setter(self):
        self.measurement.frequencies = list(range(1,101,5))

    def test_step30_frequencies_setter_with_invalid_values(self):
        with self.assertRaises(ValueError):
            self.measurement.frequencies = "1.7"


    def test_step31_sampling_time_getter(self):
        self.measurement.sampling_time

    def test_step32_sampling_time_setter(self):
        self.measurement.sampling_time = 5 * 60

    def test_step33_sampling_time_setter_with_invalid_values(self):
        with self.assertRaises(ValueError):
            self.measurement.sampling_time = "5 * 30"


    def test_step34_measurements_data(self):
        self.measurement.measurements_data

    def test_step35_time_data(self):
        self.measurement.time

    def test_step36_get_file_name(self):
        self.measurement.get_file_name()

    def test_step37_save(self):
        self.measurement.save(overwrite=True)
        print(self.measurement.get_file_name())
        self.assertTrue(self.measurement.get_file_name() and self.measurement.get_file_name().is_file())

    def test_step38_load(self):
        self.measurement.save()
        measurement = Measurement.load(self.measurement.get_file_name())
        self.assertTrue(self.measurement == measurement)

    def test_docstring(self):
        # TODO add properties
        obj = self.measurement
        for fu in dir(self.e):
            attr = getattr(obj, fu)
            if not hasattr(attr, '__call__'):
                continue
            if fu.startswith('__') and fu.endswith('__'):
                continue
            if not attr.__doc__ or attr.__doc__.strip():
                self.fail(f'No docstring for {obj.__class__.__name__}.{fu}')

if __name__ == '__main__':
    unittest.main()

