#!/usr/bin/python

import threading
import time
from util import *
import schedule
from Sensors.AI_PWM import read_ai0, read_ai1
from Sensors.BME280 import SBM280_GY39
from Sensors.GY39 import SGY39
from RelayBoard.denkovi16 import *
from DataBaseClient.type_influx import *

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

        return samples

    def send_samples_to_grafana(self):
        samples = self.read_all_sensors()

        write_to_influxdb('lux', samples[0])
        time.sleep(1)
        write_to_influxdb('tem', samples[1])
        time.sleep(1)
        write_to_influxdb('pre', samples[2])
        time.sleep(1)
        write_to_influxdb('hum', samples[3])
        time.sleep(1)
        write_to_influxdb('ai1', samples[4])
        time.sleep(1)
        write_to_influxdb('ai2', samples[5])
        time.sleep(1)
        dprint('--SensorsServiceOn--')
        dprint("lux, tem, pre, hum, ai1, ai2")
        dprint(str(samples[0])+" "+str(samples[1])+" "+str(samples[2])+" "+
               str(samples[3])+" "+str(samples[4])+" "+str(samples[5]))

    def send_samples_schedule(self):
        schedule.every(30).seconds.do(self.send_samples_to_grafana)



s = SensorService()
s.start_schedule_job(s.send_samples_schedule)

