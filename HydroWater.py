#!/usr/bin/python

import threading
import time
import schedule
from RelayBoard.denkovi16 import *


class Service:
    rb = Denkovi16()

    def start(self): pass

    def run_threaded_job(self, job_func):
        job_thread = threading.Thread(target=job_func)
        job_thread.start()

    def start_schedule_jobs(self, schedule_job1, schedule_job2):
        schedule_job1()
        schedule_job2()
        while True:
            time.sleep(0.1)
            schedule.run_pending()


class WaterService(Service):
    def water(self):
        #schedule.every(2).seconds.do(self.run_threaded_job, self.rb.give_1_liter_water)
        schedule.every().day.at("07:00").do(self.run_threaded_job, self.rb.give_1_liter_water)

    def water_smart(self):
        #schedule.every(3).seconds.do(self.run_threaded_job, self.rb.give_water_smart)
        schedule.every().day.at("08:00").do(self.run_threaded_job, self.rb.give_water_smart)


s = WaterService()
s.start_schedule_jobs(s.water, s.water_smart)
