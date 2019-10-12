#!/usr/bin/python

# GROWING LIGHT SERVICE
# Power On  the light 18[h]
# Power Off the light  6[h]



import serial
import schedule
from time import *
from RelayBoard.denkovi16 import *


class LightService:

	rb = Denkovi16()

	def day_on_18h_from_06_to_24(self):
		schedule.every(5).seconds.do(self.rb.light123_on)
		schedule.every(8).seconds.do(self.rb.light123_off)
		#schedule.every().day.at("06:00").do(self.rb.light123_on())
		#schedule.every().day.at("24:00").do(self.rb.light123_off())
	
		

	def day_off_18h_from_06_to_24(self):
		schedule.every(3).seconds.do(rb.light123_off)
		#schedule.every().day.at("06:00").do(self.rb.light123_off())
      		#schedule.every().day.at("24:00").do(self.rb.light123_on())
	
	def start(self):
		self.day_on_18h_from_06_to_24()
		while True:
			sleep(1)
			#print("----------------------------------day_on_18h_from_06_to_24----------------------------------")
			#print("----------------------------------day_off_18h_from_06_to_24----------------------------------")
			schedule.run_pending()

ls = LightService()
ls.start()
