import time

# import libti

from ._base_device import BaseDevice

class TiePieDevice(BaseDevice):
    def __init__(self):
        libtiepie.device_list.update()

        scp = None
        gen = None
        for item in libtiepie.device_list:
            if item.can_open(libtiepie.DEVICETYPE_OSCILLOSCOPE):
                scp = item.open_oscilloscope()
                if not (scp.measure_modes & libtiepie.MM_BLOCK):
                    scp = None
            if item.can_open(libtiepie.DEVICETYPE_GENERATOR):
                gen = item.open_generator()

        if not (gen and scp and len(scp.channels) >= 3):
            raise Exception('Could not find right device, please check connections. '\
                            'Check if other program uses device.')

        self.gen = gen
        self.scp = scp

        self.__name = 'tiepie device'

        self.set_generator()
        self.start_generator()
        self.set_scope()

    @property
    def name(self) -> str:
        return self.__name

    def get_data(self):
        self.scp.start()
        while not self.scp.is_data_ready:
            time.sleep(0.01)  # 10 ms delay, to save CPU time
        data = self.scp.get_data()
        time.sleep(min(0.5, 2 * 1/self.gen.frequency))
        return data

    def set_generator(self, *, frequency=1, amplitude=2, offset=0,
                            signal_type='sine'):

        if signal_type=='sine':
            self.gen.signal_type = libtiepie.ST_SINE
            self.gen.frequency = frequency # Hz
            self.gen.amplitude = amplitude # V
        elif signal_type in ('DC', 'dc', 'const', 'CONST'):
            self.gen.signal_type = libtiepie.ST_DC
        self.gen.offset = offset # V

        # Enable output:
        self.gen.output_on = True

    def start_generator(self) -> None:
        self.gen.start()

    def stop_generator(self) -> None:
        self.gen.stop()

    def set_scope(self, *, frequency=1000, scope_range=2, record_time=5) -> None:
        self.scp.trigger_time_out = 1
        self.scp.measure_mode = libtiepie.MM_BLOCK
        self.scp.sample_frequency = frequency

        self.scp.pre_sample_ratio = 0  # %

        for ch in self.scp.channels:
            ch.enabled = True
            ch.range = scope_range
            ch.coupling = libtiepie.CK_DCV  # DC Volt

        ch = self.scp.channels[0]
        ch.trigger.enabled = True
        ch.trigger.kind = libtiepie.TK_RISINGEDGE
        ch.trigger.levels[0] = 0.5  # 50 %
        ch.trigger.hystereses[0] = 0.05  # 5 %
        len_sig = frequency * record_time

        self.scp.record_length = len_sig
        self.scp.resolution = 16
