
from config import *
from util import *
from device import Device


class Denkovi16(Device):
    _br = rb_br
    _i_init_com = 1
    _all_switches_off = "off//"
    _relay_card_test = "ask//"
    _num_of_relay = 16
    _test_com = {"cmd": "off//", "ack": "off//"}

    _switches_off = {
            "1": "01-//", "2": "02-//", "3": "03-//", "4": "04-//", "5": "05-//", "6": "06-//", "7": "07-//",
            "8": "08-//", "9": "09-//", "10": "10-//", "11": "11-//", "12": "12-//", "13": "13-//",
            "14": "14-//", "15": "15-//", "16": "16-//"}

    _switches_on = {
            "1": "01+//", "2": "02+//", "3": "03+//", "4": "04+//", "5": "05+//", "6": "06+//", "7": "07+//",
            "8": "08+//", "9": "09+//", "10": "10+//", "11": "11+//", "12": "12+//", "13": "13+//",
            "14": "14+//", "15": "15+//", "16": "16+//"}

    def __init__(self):
        super().__int__()

    def init_board(self):
        if rb_flag:
            if self.send_and_wait(self._all_switches_off, self._all_switches_off) == 0:#b'off//'
                if self.send_and_wait(self._relay_card_test, "") == 0:#b''
                    self.logger.debug("pass")
                    return 0
                else:
                    self.logger.debug("fail")
                    return -1
            else:
                self.logger.debug("fail")
                return -1

    # Switch On =1, Switch Off=0 .
    def set_switch(self, switch_num, mode):
        if rb_flag:
            assert 1 <= switch_num <= self._num_of_relay, " No switch like this"
            if mode == 1:  # Switch On.
                feedback = self._switches_on[str(switch_num)]
                if self.send_and_wait(self._switches_on[str(switch_num)], feedback) == 0:
                    self.logger.debug(" number " + str(switch_num) + " on pass")
                    return 0
                else:
                    self.logger.debug("fail")
                    return -1
            else:  # Switch Off.
                feedback = self._switches_off[str(switch_num)]
                if self.send_and_wait(self._switches_off[str(switch_num)], feedback) == 0:
                    self.logger.debug(" number " + str(switch_num) + " off pass")
                    return 0
                else:
                    self.logger.debug("fail")
                    return -1

    def light1_off(self):
        return self.set_switch(light1, 0)

    def light1_on(self):
        return self.set_switch(light1, 1)

    def motor_off(self):
        return self.set_switch(motor, 0)

    def motor_on(self):
        return self.set_switch(motor, 1)

    def buzzer_off(self):
        return self.set_switch(buzzer, 0)

    def buzzer_on(self):
        return self.set_switch(buzzer, 1)

    def pneumatic_off(self):
        return self.set_switch(pneumatic, 0)

    def pneumatic_on(self):
        return self.set_switch(pneumatic, 1)

    def lda_off(self):
        return self.set_switch(lda, 0)

    def lda_on(self):
        return self.set_switch(lda, 1)

    def fan_off(self):
        return self.set_switch(fan, 0)

    def fan_on(self):
        return self.set_switch(fan, 1)

    def sniffer_off(self):
        return self.set_switch(sniffer, 0)

    def sniffer_on(self):
        return self.set_switch(lda, 1)

    def getway_off(self):
        return self.set_switch(lda, 0)

    def getway_on(self):
        return self.set_switch(lda, 1)

    def light123_off(self):
        return self.set_switch("04-//", 0)

    def light123_on(self):
        return self.set_switch("04+//", 1)

    def test_device(self):
        self.lda_on()
        time.sleep(2)
        self.lda_off()
        time.sleep(2)
        self.light1_on()
        time.sleep(2)
        self.light1_off()

# Test class.
# r = Denkovi16().test_device()
