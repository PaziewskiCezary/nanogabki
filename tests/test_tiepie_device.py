import unittest

from electrode_tester.device import TiePieDevice

class TiePieDeviceTest(unittest.TestCase):

    def setUp(self):
        self.device = TiePieDevice()

    def test_name(self):
        self.assertEqual(self.name, 'tiepie device')

    def test_set_generator():
        self.device.set_generator()

    def test_set_scope():
        self.device.set_scope()

    def test_set_generator():
        self.device.set_generator()

    def get_data():
        self.device.get_data()

    def stop_generator():
        self.device.stop_generator()

    def test_docstring(self):
        # TODO add properties
        obj = self.device
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

