#!/usr/bin/python

import threading
import time
import schedule
from Sensors.AI_PWM import read_ai0, read_ai1
from Sensors.BME280 import SBM280_GY39
from Sensors.GY39 import SGY39
from RelayBoard.denkovi16 import *

class Service:
    rb = Denkovi16()

    def start(self): pass

    def run_threaded_job(self, job_func):
        job_thread = threading.Thread(target=job_func)
        job_thread.start()

    def start_schedule_job(self, schedule_job1):
        schedule_job1()
        while True:
            time.sleep(0.1)
            schedule.run_pending()



class SensorService(Service):

    s1 = SGY39(1, 0x4A, 'lux')
    s2 = SBM280_GY39(1, 0x76, 'C hPa %')

    def read_all_sensors(self):
        lux = self.s1.get_sample()
        tem, pre, hum = self.s2.get_sample()
        ai1 = read_ai0()
        ai2 = read_ai1()
        # ph = read_ph()
        # wle = read_water_level()

        samples = [lux, tem, pre, hum, ai1, ai2]
        print("lux, tem, pre, hum, ai1, ai2]")
        print(samples)

    def send_samples_to_grafana(self):
        schedule.every(2).seconds.do(self.read_all_sensors)

s = SensorService()
s.start_schedule_job(s.send_samples_to_grafana)

