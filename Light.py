#!/usr/bin/python

# GROWING LIGHT SERVICE
# Power On  the light 18[h]
# Power Off the light  6[h]


import threading
import time
import serial
import schedule
from RelayBoard.denkovi16 import *
from util import *
from cfg import *


# GDP    1     2     3
#on  1 2 3 4 5 6 7 8 9 10
#        10     10     10
#0ff 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
#         0     0     0
#on  1 2 3 4 5 6 7 8 9 10
#        1     1     1
#0ff 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
#         0     0     0





class Service:
	rb = Denkovi16()

	def run_threaded(self, job_func):
		job_thread = threading.Thread(target=job_func)
		job_thread.start()

class LightGrowService(Service):
	def start(self):
		# schedule.every().day.at("06:00").do(self.rb.light123_on)
		# schedule.every().day.at("24:00").do(self.rb.light123_off)
		schedule.every(3).seconds.do(self.rb.light123_on_grow)
		schedule.every(3.8).seconds.do(self.rb.light123_off_grow)


class LightFlowService(Service):
	def start(self):
		# schedule.every().day.at("06:00").do(self.rb.light123_on)
		# schedule.every().day.at("24:00").do(self.rb.light123_off)

		schedule.every(3).seconds.do(self.rb.light123_on_flow)
		schedule.every(3.8).seconds.do(self.rb.light123_off_flow)


grow = LightGrowService()
flow = LightFlowService()

grow.start()
flow.start()

while True:
	time.sleep(0.1)
	schedule.run_pending()