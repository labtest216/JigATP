#!/usr/bin/python3
from random import *
import serial
import serial.tools.list_ports
from util import *
from cfg import *
from time import sleep


def get_my_com():
    coms = []
    coms = serial.tools.list_ports.comports()
    for com in coms:
        print(str(com))
        print(str(com.name))
        print(str(com.device))
        if "FT232R USB UART" in com:
            os.system('sudo chmod 777 ' + str(com.device))
            os.system('sudo chmod 777 /dev/i2c-*')
            dprint("find com:" + str(com))
            return str(com.device)


def dmode(mode):
    if mode == 1:
        return "on"
    else:
        return "off"


class Denkovi16:
    counter = 0
    _i_init_com = 1

    _all_switches_off = "off//"
    _relay_card_test = "ask//"
    _num_of_relay = 16
    _test_com = {"cmd": "off//", "ack": "off//"}

    _map_sw = {"1": "Venta", "2": "Water_Pump", "3": "SW3_220v", "4": "Light",
            "5": "SW5_5v", "6": "SW6_5v", "7": "SW7_5v", "8": "SW8_5v",
            "9": "Fan1", "10": "Fan2", "11": "Fan3", "12": "Air_Pump",
            "13": "SW13_3v", "14": "SW14_3v", "15": "SW15_3v", "16": "SW16_24v"}

    _switches_off = {
        "1": "01-//", "2": "02-//", "3": "03-//", "4": "04-//", "5": "05-//", "6": "06-//", "7": "07-//",
        "8": "08-//", "9": "09-//", "10": "10-//", "11": "11-//", "12": "12-//", "13": "13-//",
        "14": "14-//", "15": "15-//", "16": "16-//"}

    _switches_on = {
        "1": "01+//", "2": "02+//", "3": "03+//", "4": "04+//", "5": "05+//", "6": "06+//", "7": "07+//",
        "8": "08+//", "9": "09+//", "10": "10+//", "11": "11+//", "12": "12+//", "13": "13+//",
        "14": "14+//", "15": "15+//", "16": "16+//"}

    def __init__(self):
        com = str(get_my_com())
        self._com = serial.Serial(port=com, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1)  #

    def get_sw(self, sw):
        return self._map_sw[str(sw)]

    def init_com(self):
        try:
            if self._com.is_open:
                dprint(f_name() + ' pass')
                return 0
            else:
                self._com.open()
                dprint(f_name() + ' pass')
            return 0
        except:
            return -2

    def get_sw_status(self):
        try:
            counter = 0
            read_buf = self.send_and_get(self._relay_card_test)
            if int(len(read_buf)) != 2:
                counter += 1
                read_buf = self.send_and_get(self._relay_card_test)
                if counter > 3:
                    return -1
            sw1to8 = str(bin(read_buf[0])[2:].zfill(8))
            sw9to16 = str(bin(read_buf[1])[2:].zfill(8))

            dprint(sw1to8)
            dprint(sw9to16)
            return sw1to8, sw9to16

        except Exception as e:
            print('Exception ' + str(f_name()) + str(e))

    def send_and_get(self, data_to_send):
        dprint(self.get_class_name() + " send " + data_to_send)
        self._com.write(data_to_send.encode("ascii"))
        read_buf = self._com.read_until()
        return read_buf

    def send_and_wait(self, data_to_send, data_to_get):
        sleep(0.5)
        # dprint(self.get_class_name() + " send " + data_to_send + " wait for " + data_to_get)
        self._com.write(data_to_send.encode("ascii"))
        read_buf = self._com.read(size=len(data_to_get)).decode("ascii")
        # dprint(self.get_class_name() + " receive " + str(read_buf))
        if read_buf == data_to_get:
            return 0
        else:  # Try resend and wait for ack.
            sleep(0.5)
            self._com.write(data_to_send.encode("ascii"))
            read_buf = self._com.read(size=len(data_to_get)).decode("ascii")
            # dprint(self.get_class_name() + " send " + data_to_send + " wait for " + data_to_get)
            # dprint(self.get_class_name() + " receive " + str(read_buf))
            if read_buf == data_to_get:
                return 0
            else:
                # dprint(self.get_class_name() + " not get ack")
                return -1

    def get_class_name(self):
        name = str(type(self).__name__)
        return name

    def init_board(self):
        if self.send_and_wait(self._all_switches_off, self._all_switches_off) == 0:  # b'off//'
            dprint(f_name() + " pass")
            return 0
        else:
            dprint(f_name() + " fail")
            return -1

    # Switch On =1, Switch Off=0 .
    def set_switch(self, switch_num, mode):

        try:
            sleep(0.5)
            # Open com.
            #self.init_com()
            assert 1 <= switch_num <= self._num_of_relay, " No switch like this"
            if mode == 1:  # Switch On.
                feedback = self._switches_on[str(switch_num)]
                if self.send_and_wait(self._switches_on[str(switch_num)], feedback) == 0:
                    # dprint(" number " + str(switch_num) + " on pass")
                    # Close com.
                    #self._com.close()
                    return 0
                else:
                    # dprint("fail")
                    # Close com.
                    #self._com.close()
                    return -1
            else:  # Switch Off.
                feedback = self._switches_off[str(switch_num)]
                if self.send_and_wait(self._switches_off[str(switch_num)], feedback) == 0:
                    # dprint(" number " + str(switch_num) + " off pass")
                    # Close com.
                    #self._com.close()
                    return 0
                else:
                    # dprint("fail")
                    # Close com.
                    #self._com.close()
                    return -1
        except Exception as e:
            self.counter += 1
            # print(str(self.counter))
            # Wait random time and try again.
            time.sleep(random())
            if self.counter < 2:
                self.set_switch(switch_num, mode)
            else:
                print('Exception ' + str(f_name()) + str(e))
                return -1

    def give_water_smart(self):
        sens1 = config_file(cfg_json, "SensCon1", "get")
        sens2 = config_file(cfg_json, "SensCon2", "get")
        if int(sens1) < 100:
            if int(sens2) < 100:
                dprint('--SmartWaterServiceOn--')
                self.set_switch(sw_water, 1)
                time.sleep(6)
                dprint('--SmartWaterServiceOff--')
                self.set_switch(sw_water, 0)

    def light(self, mode):
        return self.dbug(mode, str(f_name()), sw_light)

    def waterpump(self, mode):
        return self.dbug(mode, str(f_name()), sw_water)

    def airpump(self, mode):
        return self.dbug(mode, str(f_name()), sw_airpu)

    def venta(self, mode):
        return self.dbug(mode, str(f_name()), sw_venta)

    def fain1(self, mode):
        return self.dbug(mode, str(f_name()), sw_fansm)

    def fain2(self, mode):
        return self.dbug(mode, str(f_name()), sw_fanlr)

    def fain3(self, mode):
        return self.dbug(mode, str(f_name()), sw_fanxl)

    def motor(self, mode):
        return self.dbug(mode, str(f_name()), sw_motor)

    def dbug(self, mode, fname, sw):
        m = dmode(mode)
        if self.set_switch(sw, mode) == 0:
            dprint(fname + " " + str(m) + " pass")
            return 0
        else:
            dprint(fname + " " + str(m) + " fail")
            return -1
