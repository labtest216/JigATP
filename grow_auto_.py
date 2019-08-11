#!/usr/bin/python
import RPi.GPIO as GPIO
import time,os,sys
import serial
import utils
import binascii
from utils import dprint
from utils import f_name



class AutoGrow:
	all_relay_off="off//"	
	relay_card_test="ask//"
	read_buf="" 
    	
 # Initial com port, Turn on ER16 board.
	def __init__(self):
		self.com=serial.Serial("/dev/ttyUSB0", baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2)
		self.init_gpio()
		if self.com.is_open:
			dprint("Comunication with ER16 open")
			self.init_relay_card()
		else:
			dprint("Com can not open - Can not comunicate with ER16")
        
 # Init GPIO.
	def init_gpio(self):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(3, GPIO.OUT)
		GPIO.output(3, False)

	     
# Power off all relay in case of bug.            
	"""def safty_poweroff(self):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(2, GPIO.OUT)
		GPIO.output(2, True)
		dprint(f_name()+" No feedback from ER16 after retry")
		self.com.close()
	if not com.is_open:
    		dprint("Comunication with ER16 close")
	else:
    		dprint("Can not close com")        """
        
# Initial relay cards.
	def init_relay_card(self):
		if self.send_and_wait(self.all_relay_off,"off") == 0:
			if self.send_and_wait(self.relay_card_test,"\x00\x00") == 0:
				dprint(f_name()+" pass")
				return 0
			else:
				dprint(f_name() +" fail")
				return -1
		else:
			dprint(f_name() +" fail")
			return -1
            
            
# Validate ER16 feedback.
	def send_and_wait(self, data, feedback):
		if self.com.is_open:
			self.com.write(str.encode(data))
			dprint("Rpi send: "+data)
			self.read_buf = self.com.readline()
			dprint("Rpi get: "+str(self.read_buf))
			if str(self.read_buf).find(feedback)==-1:
				dprint("Retrying to get feedback from ER16")
				time.sleep(1)
				self.com.write(str.encode(data))
				dprint("Rpi send: "+data)
				self.read_buf = str(self.com.readline())
				dprint("Rpi get: "+self.read_buf)
				if str(self.read_buf).find(feedback)==-1:                            
#		                        self.safty_poweroff()
		                        dprint(f_name()+" fail")
		                        return -1
				else:
					dprint(f_name()+" pass")
					return 0
			else:
				dprint(f_name()+" pass")
				return 0
		else:
			dprint(f_name()+" fail")
			return -1
            
# Relay 1-8: num= "00"-"16" mode: close=1, open=0 .
	def relay_set(self, relay_num, relay_mode):
		if(relay_mode==1):#close.
		    cmd=str(relay_num)+"+//"
		    if self.send_and_wait(cmd, relay_num+"+")==0:
		        dprint(f_name()+" pass")
		        return 0
		    else:
		        dprint(f_name()+" fail")
		        return -1
		else:#open.
		    cmd=str(relay_num)+"-//"
		    if self.send_and_wait(cmd, relay_num+"-")==0:
		        dprint(f_name()+" pass")
		        return 0
		    else:
		        dprint(f_name()+" fail")
		        return -1
            
# Led set RL1 220v
	def led_on(self):
		if self.relay_set("01", 1)==0:
			dprint(f_name()+" pass")
			return 0
		else:
 			dprint(f_name()+" fail")
 			return -1
		
	def led_off(self):
		if self.relay_set("01", 0)==0:
			dprint(f_name()+" pass")
			return 0
		else:
			dprint(f_name()+" fail")
			return -1
            
# Water set RL13 5v->24v->220v-Water Pump.
	def water_on(self):
		if self.relay_set("13", 1)==0:
			dprint(f_name()+" pass")
			return 0
		else:
			dprint(f_name()+" fail")
			return -1
		    
	def water_off(self):
		if self.relay_set("13", 0)==0:
			dprint(f_name()+" pass")
			return 0
		else:
			dprint(f_name()+" fail")
			return -1
        
#Sprinkler set RL3.
	def sprinkler_on(self):
		if self.relay_set("03", 1) == 0:
		    dprint(f_name()+" pass")
		    return 0
		else:
		    dprint(f_name()+" fail")
		    return -1

	def sprinkler_off(self):
		if self.relay_set("03", 0)==0:
			dprint(f_name()+" pass")
			return 0
		else:
			dprint(f_name()+" fail")
			return -1

#Fan set RL4 5v->24v->220v-Led..
	def fan_on(self):
		if self.relay_set("14", 1)==0:
			dprint(f_name()+" pass")
			return 0
		else:
			dprint(f_name()+" fail")
			return -1

	def fan_off(self):
		if self.relay_set("14", 0)==0:
			dprint(f_name()+" pass")
			return 0
		else:
			dprint(f_name()+" fail")
			return -1

	def beep(self, beep_time):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(3, GPIO.OUT)
		GPIO.output(3, True)
		time.sleep(beep_time)
		GPIO.output(3, False)
	
	


"""
    # A/D
    def measure_temp(self):

    def measure_humidity(self):

    def measure_light(self):
  """  
		






"""while True:
	time.sleep(1)
	com.write("test\r\n")
	self.read_buf=read_line(com)
	time.sleep(1)
	print(self.read_buf)
	


os.system("pinout")
while True:
	time.sleep(2)
	GPIO.output(2, False)
	time.sleep(2)
	GPIO.output(2, True)"""


