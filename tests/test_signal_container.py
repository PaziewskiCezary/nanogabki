from electrode_tester._signal_container import SignalContainer


class SignalContainerTest(unittest.TestCase):

    def setUp(self):
       pass


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
