#!/usr/bin/python
from cfg import *
from util import *
import serial
import serial.tools.list_ports
from random import *

class Denkovi16:
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
        self._com.baudrate=9600
        self._com.port='/dev/ttyUSB0'
        self._com.bytesize=8
        self._com.parity='N'
        self._com.stopbits=1
        self._com.timeout=0.2

    def get_com(self):
        try:
            comlist = serial.tools.list_ports.comports()
            connected_com = []
            for element in comlist:
                connected_com.append(element.device)
            print("Connected COM ports: " + str(connected_com))

            for com in connected_com:
                if self.init_com(self._com, self._br) == 0:  # Try init com.
                    if self.init_board() == 0:  # Try test com.
                        print(self.get_class_name() + " :" + str(com))
                        self._com.name = str(com)
                        self._com.close()
                        return str(com)
                    else:
                        print('fail')
                        return -1
                else:  # Try next com.
                    self._com.close()
        except Exception as e:
            print(e)

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
            # Wait random time and try again.
            time.sleep(random())
            self.set_switch(switch_num, mode)


    def light123_off(self):
        return self.set_switch(4, 0)

    def light123_on(self):
        return self.set_switch(4, 1)

    def test_device(self):
        self.light123_on()
        time.sleep(2)
        self.light123_off()
        time.sleep(2)
# ---------------------------------------------------------------------

    def light123_on_grow(self):
        print('-----------------------GrowServiceOn------------------------')
        GrowDaysPass = config_file(cfg_json, "GrowDaysPass", "get")
        GrowEnd = config_file(cfg_json, "GrowEnd", "get")

        if int(GrowEnd) == 0:
            if int(GrowDaysPass) < int(GrowDays):
                return self.set_switch(4, 1)

    def light123_off_grow(self):
        print('-----------------------GrowServiceOff------------------------')
        GrowDaysPass = config_file(cfg_json, "GrowDaysPass", "get")
        GrowEnd = config_file(cfg_json, "GrowEnd", "get")
        print("light123_off_grow: GrowDays=" + str(GrowDays) + " GrowDaysPass=" + GrowDaysPass + " GrowEnd=" + GrowEnd)

        if int(GrowEnd) == 0:
            if int(GrowDaysPass) == int(GrowDays):
                config_file(cfg_json, "GrowEnd", 1)
                return self.set_switch(4, 0)
            elif int(GrowDaysPass) < int(GrowDays):
                config_file(cfg_json, "GrowDaysPass", int(GrowDaysPass) + 1)
                return self.set_switch(4, 0)
        else:
            print("GrowEnd")
#---------------------------------------------------------------------

    def light123_on_flow(self):
        print('-----------------------FlowServiceOn------------------------')
        GrowEnd = config_file(cfg_json, "GrowEnd", "get")
        FlowEnd = config_file(cfg_json, "FlowEnd", "get")
        FlowDaysPass = config_file(cfg_json, "FlowDaysPass", "get")

        if int(GrowEnd):
            if int(FlowEnd) == 0:
                if int(FlowDaysPass) < int(FlowDays):
                    return self.set_switch(4, 1)

    def light123_off_flow(self):
        print('-----------------------FlowServiceOff------------------------')
        GrowEnd = config_file(cfg_json, "GrowEnd", "get")
        FlowEnd = config_file(cfg_json, "FlowEnd", "get")
        FlowDaysPass = config_file(cfg_json, "FlowDaysPass", "get")
        print("light123_on_flow: FlowDays=" + str(FlowDays) + " GrowDaysPass=" + FlowDaysPass + " GrowEnd" + GrowEnd)

        if int(GrowEnd):
            if int(FlowEnd) == 0:
                if int(FlowDaysPass) == int(FlowDays):
                    config_file(cfg_json, "FlowEnd", 1)
                    return self.set_switch(4, 0)
                elif int(FlowDaysPass) < int(FlowDays):
                    config_file(cfg_json, "FlowDaysPass", int(FlowDaysPass) + 1)
                    return self.set_switch(4, 0)
            else:
                print("FlowEnd")

#---------------------------------------------------------------------
    def give_1_liter_water(self):
        print('-----------------------WaterService ------------------------')
        # Pump=5Liter to 60 seconds.
        # 1Liter to 60/5=12
        # Mix water with food by motor.

        # Start motor.
        #self.set_switch(5, 1)
        #time.sleep(12)

        # Start pump
        self.set_switch(9, 1)
        time.sleep(12)
        # Stop pump.
        self.set_switch(9, 0)
        # Stop motor.
        #time.sleep(2)
        # self.set_switch(5, 0)

    def give_water_smart(self):
        if
        self.set_switch(9, 0)
            time.sleep(5)


"""
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

"""

# Test class.
#r = Denkovi16()
#r.test_device()
#r.get_com()
