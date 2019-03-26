from config import *
from util import *
from device import Device

class Odroid(Device):
    _br = gw_br
    _i_init_com = 1
    _test_com = {"cmd": "Odroid_Test_Com\n", "ack": "Odroid_Test_Ok\n"}
    _get_sht31 = {"cmd": "Get_SHT31_TH\n", "ack": "SHT31_Ok\n"}

    def __init__(self):
        super().__int__()

    def get_i2c(self, addr, bus):
        print("not imp")

    def set_io(self, pin, mode):
        print("not imp")

    def read_ai(self, pin):
        print("not imp")

    def read_sht31(self):
        th = self.send_and_get(self._get_sht31["cmd"])
        return th

    def test_device(self):
        self.send_and_get(self._test_com["cmd"], self._test_com["ack"])
        self.read_sht31()

# Test class.
o = Odroid().test_com()