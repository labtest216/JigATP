import time
from util import *
from serial import Serial
from config import *
from device import Device


class Motor(Device):
    _br = m_br
    _i_init_com = 1
    _test_com = {"cmd": stop, "ack": stop_ok}

    def __init__(self):
        super().__int__()


    def start(self):
        return self.send_and_wait(start, start_ok)

    def stop(self):
        return self.send_and_wait(stop, stop_ok)

    def set_speed(self, speed_num):
        return self.send_and_wait(speed+str(speed_num), speed_ok)

    def set_dir(self, dir):
        if dir is True:
            return self.send_and_wait(pdir, dir_ok)
        else:
            return self.send_and_wait(ndir, dir_ok)

    def invert_dir(self):
        return self.send_and_wait(invert_dir, dir_ok)

    def test_device(self):
        self.start()
        time.sleep(2)
        self.set_speed(222)
        time.sleep(2)
        self.invert_dir()
        time.sleep(2)
        self.set_dir(True)
        time.sleep(2)
        self.set_dir(False)
        time.sleep(2)
        self.stop()


# Test class.
m = Motor()

