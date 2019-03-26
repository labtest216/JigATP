import time
from device import Device
from config import *


class LedAnalyzer(Device):
    _br = lda_br
    _i_init_com = 1
    _test_com = {"cmd": "testcon\r", "ack": "OK\r"}

    # Commands and commands ack.
    _get_hw_ver = {"cmd": "gethw\r", "ack": "GPS 5-1\r"}
    _test_com = {"cmd": "testcon\r", "ack": "OK\r"}
    _get_serial = {"cmd": "getserial\r", "ack": "1625\r"}
    _get_sw_ver = {"cmd": "getversion\r", "ack": "2002\r"}
    _set_capture_time_11ms = {"cmd": "setcaptime11\r", "ack": "OK\r"}
    _set_capture_time_600ms = {"cmd": "setcaptime600\r", "ack": "OK\r"}
    _capture_all_ports = {"cmd": "capture\r", "ack": "OK\r"}

    def __init__(self):
        super().__int__()

    def init_board(self):
        cmd = self._get_serial["cmd"]
        ack = self._get_serial["ack"]
        if self.send_and_wait(cmd, ack) == 0:
            self.logger.debug("pass")
            return 0
        else:
            self.logger.debug("fail")
            return -1

    # HUE_RED<40 310<HUE_RED<360; 80<HUE_GRN<160;  220<HUE_BLU<260; 50<HUE_YEL<70
    # 0<Saturation<999
    # 0<Intensity<99999
    def get_hsi_rgbi_xy(self, port, value=None):
        gethsi = "gethsi" + str(port) + " 1\r"
        getrgbi = "getrgbi" + str(port) + " 1\r"
        getxy = "getxy" + str(port) + " 1\r"

        self.send_and_wait(self._capture_all_ports["cmd"], self._capture_all_ports["ack"])
        hsi = self.send_and_get(gethsi)
        hsi = hsi[0:len(hsi)-1]
        rgbi = self.send_and_get(getrgbi)
        rgbi = rgbi[0:len(rgbi)-1]
        xy = self.send_and_get(getxy)
        xy = xy[0:len(xy)-1]
        hue, saturation, intensity, red, grn, blu, intensity, x, y = self.parse_values(self, hsi, rgbi, xy)

        if value == "hsi":
            return hue, saturation, intensity
        elif value == "rgbi":
            return red, grn, blu, intensity
        elif value == "xy":
            return x, y
        else:
            return hue, saturation, intensity, red, grn, blu, intensity, x, y

    @staticmethod
    def parse_values(self, hsi, rgbi, xy):
        hue, saturation, intensity = str(hsi).split(" ")
        red, grn, blu, intensity = str(rgbi).split(" ")
        x, y = str(xy).split(" ")
        self.logger.debug("hue=" + str(hue) + " saturation=" + str(saturation) + " intensity=" + str(intensity))
        self.logger.debug(" red=" + str(red) + " grn=" + str(grn) + " blu=" + str(blu) + " x=" + str(x)+" y=" + str(y))
        return hue, saturation, intensity, red, grn, blu, intensity, x, y



    def test_device(self):
        self.get_hsi_rgbi_xy(1)

# Test class.
r = LedAnalyzer().test_device()
