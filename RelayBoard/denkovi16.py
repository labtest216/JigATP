#!/usr/bin/python3

import serial
import serial.tools.list_ports
from util import * 

class Denkovi16:
	_i_init_com = 1
	_com = '/dev/ttyUSB0'
	_br = 9600

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


	#def __init__(self):
		#self.init_com()
  

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
		except Exception as e: print(e)

	def init_com(self,com ,br):
		try:
			self._com = serial.Serial(port=com, baudrate=br, bytesize=8, parity='N', stopbits=1, timeout=2)  #
			if self._com.is_open:
				self.logger.debug('pass')
				return 0
			else:
				self.logger.debug('fail')
			return -1
		except:
			return -2

	def send_and_get(self, data_to_send):
		self.logger.debug(self.get_class_name() + " send " + data_to_send)
		self._com.write(data_to_send.encode("ascii"))
		read_buf = self._com.read_until()
		return read_buf.decode()

	def send_and_wait(self, data_to_send, data_to_get):
		self.logger.debug(self.get_class_name() + " send " + data_to_send+" wait for " + data_to_get)
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
		if self.send_and_wait(self._all_switches_off, self._all_switches_off) == 0:#b'off//'
			self.logger.debug("pass")
			return 0
		else:
			self.logger.debug("fail")
			return -1


	# Switch On =1, Switch Off=0 .
	def set_switch(self, switch_num, mode):
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

	def light123_off(self):
		return self.set_switch(4, 0)

	def light123_on(self):
		return self.set_switch(4, 1)

	def test_device(self):
		self.light123_on()
		time.sleep(2)
		self.light123_off()
		time.sleep(2)


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
