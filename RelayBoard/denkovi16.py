#!/usr/bin/python3
from random import *
import serial
import serial.tools.list_ports
from util import *
from cfg import *


class Denkovi16:
    counter = 0
    _i_init_com = 1

    _all_switches_off = "off//"
    _relay_card_test = "ask//"
    _num_of_relay = 16
    _test_com = {"cmd": "off//", "ack": "off//"}

    logger = init_logger("RelayBoard")

    _switches_off = {
        "1": "01-//", "2": "02-//", "3": "03-//", "4": "04-//", "5": "05-//", "6": "06-//", "7": "07-//",
        "8": "08-//", "9": "09-//", "10": "10-//", "11": "11-//", "12": "12-//", "13": "13-//",
        "14": "14-//", "15": "15-//", "16": "16-//"}

    _switches_on = {
        "1": "01+//", "2": "02+//", "3": "03+//", "4": "04+//", "5": "05+//", "6": "06+//", "7": "07+//",
        "8": "08+//", "9": "09+//", "10": "10+//", "11": "11+//", "12": "12+//", "13": "13+//",
        "14": "14+//", "15": "15+//", "16": "16+//"}

    def __init__(self):
        #self.init_com(self._com, self._br)
        #self._com = serial.Serial(port=com, baudrate=br, bytesize=8, parity='N', stopbits=1, timeout=1)  #
        self._com = serial.Serial()
        self._com.baudrate = 9600
        self._com.port = '/dev/ttyUSB0'
        self._com.bytesize = 8
        self._com.parity = 'N'
        self._com.stopbits = 1
        self._com.timeout = 0.2



    def init_com(self, com, br):
        try:
            if self._com.is_open:
                self.logger.debug('pass')
                return 0
            else:
                self._com.open()
                self.logger.debug('pass')
            return 0
        except:
            return -2

    def send_and_get(self, data_to_send):
        self.logger.debug(self.get_class_name() + " send " + data_to_send)
        self._com.write(data_to_send.encode("ascii"))
        read_buf = self._com.read_until()
        return read_buf.decode()

    def send_and_wait(self, data_to_send, data_to_get):
        self.logger.debug(self.get_class_name() + " send " + data_to_send + " wait for " + data_to_get)
        self._com.write(data_to_send.encode("ascii"))
        read_buf = self._com.read(size=len(data_to_get)).decode("ascii")
        self.logger.debug(self.get_class_name() + " receive " + str(read_buf))
        if read_buf == data_to_get:
            return 0
        else:  # Try resend and wait for ack.
            self._com.write(data_to_send.encode("ascii"))
            read_buf = self._com.read(size=len(data_to_get)).decode("ascii")
            self.logger.debug(self.get_class_name() + " send " + data_to_send + " wait for " + data_to_get)
            self.logger.debug(self.get_class_name() + " receive " + str(read_buf))
            if read_buf == data_to_get:
                return 0
            else:
                self.logger.debug(self.get_class_name() + " not get ack")
            return -1

    def get_class_name(self):
        name = str(type(self).__name__)
        return name

    def init_board(self):
        if self.send_and_wait(self._all_switches_off, self._all_switches_off) == 0:  # b'off//'
            self.logger.debug("pass")
            return 0
        else:
            self.logger.debug("fail")
            return -1

    # Switch On =1, Switch Off=0 .
    def set_switch(self, switch_num, mode):

        try:
            # Open com.
            self._com.open()
            assert 1 <= switch_num <= self._num_of_relay, " No switch like this"
            if mode == 1:  # Switch On.
                feedback = self._switches_on[str(switch_num)]
                if self.send_and_wait(self._switches_on[str(switch_num)], feedback) == 0:
                    self.logger.debug(" number " + str(switch_num) + " on pass")
                    # Close com.
                    self._com.close()
                    return 0
                else:
                    self.logger.debug("fail")
                    # Close com.
                    self._com.close()
                    return -1
            else:  # Switch Off.
                feedback = self._switches_off[str(switch_num)]
                if self.send_and_wait(self._switches_off[str(switch_num)], feedback) == 0:
                    self.logger.debug(" number " + str(switch_num) + " off pass")
                    # Close com.
                    self._com.close()
                    return 0
                else:
                    self.logger.debug("fail")
                    # Close com.
                    self._com.close()
                    return -1
        except:
            self.counter += 1
            print(str(self.counter))
            # Wait random time and try again.
            time.sleep(random())
            if self.counter < 2:
                self.set_switch(switch_num, mode)
            else:
                print('Exception ' + str(f_name()))
                return -1

    def give_water_smart(self):
        sens1 = config_file(cfg_json,"SensCon1", "get")
        sens2 = config_file(cfg_json,"SensCon2", "get")
        if int(sens1) < 100:
            if int(sens2) < 100:
                dprint('--SmartWaterServiceOn--')
                self.set_switch(sw_water, 1)
                time.sleep(6)
                dprint('--SmartWaterServiceOff--')
                self.set_switch(sw_water, 0)



