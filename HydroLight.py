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


class Service:
	rb = Denkovi16()

	def start(self): pass

	def run_threaded_job(self, job_func):
		job_thread = threading.Thread(target=job_func)
		job_thread.start()

	def start_schedule_jobs(self, schedule_job1,schedule_job2):
		schedule_job1()
		schedule_job2()
		while True:
			time.sleep(0.1)
			schedule.run_pending()


class LightService(Service):
	def grow(self):

		# schedule.every().day.at("06:00").do(self.run_threaded_job, self.rb.light123_on_grow)
		# schedule.every().day.at("24:00").do(self.run_threaded_job, self.rb.light123_off_grow)

		schedule.every(3).seconds.do(self.run_threaded_job, self.rb.light123_on_grow)
		schedule.every(5).seconds.do(self.run_threaded_job, self.rb.light123_off_grow)

	def flow(self):
		# schedule.every().day.at("06:00").do(self.run_threaded_job, self.rb.light123_on_flow)
		# schedule.every().day.at("24:00").do(self.run_threaded_job, self.rb.light123_off_flow)

		schedule.every(7.2).seconds.do(self.run_threaded_job, self.rb.light123_on_flow)
		schedule.every(11).seconds.do(self.run_threaded_job, self.rb.light123_off_flow)

s = LightService()
s.start_schedule_jobs(s.grow, s.flow)


