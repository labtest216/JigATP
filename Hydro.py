#!/usr/bin/python3
import os
import sys


def add_python_path():
    print(sys.path)
    paths = []

    for path in paths:
        print(sys.path.append(path))
    print(sys.path)


add_python_path()

from influxdb import InfluxDBClient
import time
import schedule
from denkovi16 import *
from util import *
from ADC_ADS115 import *
from AI_PWM import *
from BME280 import *
from GY39 import *
from SHT31 import *

class HydroService:
    rb = Denkovi16()
    s1 = SGY39(1, 0x4A, 'lux')
    s2 = SBM280_GY39(1, 0x76, 'C hPa %')
    s3 = SADS115(2, 0x48, 'v')
    s4 = SADS115(2, 0x49, 'v')

    def __init__(self):
        self.rb.waterpump(0)

    def start_schedule_jobs(self):
        # Motor   on/off.
        schedule.every().day.at("07:00").do(self.rb.motor, mode=1)
        schedule.every().day.at("07:01").do(self.rb.motor, mode=0)
        # Water   on/off.
        schedule.every().day.at("07:02:00").do(self.rb.waterpump, mode=1)
        schedule.every().day.at("07:02:12").do(self.rb.waterpump, mode=0)
        schedule.every().day.at("07:05").do(self.rb.waterpump, mode=0)
        schedule.every().day.at("07:06").do(self.rb.waterpump, mode=0)

        # Light   on/off.
        # Grow:
        schedule.every().day.at("05:30").do(self.rb.light, mode=1)
        schedule.every().day.at("23:30").do(self.rb.light, mode=0)
        # Flow:
        #schedule.every().day.at("05:00").do(self.rb.light, mode=1)
        #schedule.every().day.at("17:00").do(self.rb.light, mode=0)

        # Venta   on/off.
        schedule.every().day.at("08:00").do(self.rb.venta, mode=1)
        schedule.every().day.at("16:00").do(self.rb.venta, mode=0)

        # AirPump on/off.
        schedule.every().day.at("08:00").do(self.rb.airpump, mode=1)
        schedule.every().day.at("09:00").do(self.rb.airpump, mode=0)
        schedule.every().day.at("18:00").do(self.rb.airpump, mode=1)
        schedule.every().day.at("19:00").do(self.rb.airpump, mode=0)

        # Sensors on/off.
        schedule.every(3).seconds.do(self.send_samples_to_grafana)

        while True:
            time.sleep(0.1)
            schedule.run_pending()



    def read_all_sensors(self):
        try:
            lux = self.s1.get_sample()
            tem, pre, hum = self.s2.get_sample()

            ai1 = read_ai0()
            ai2 = read_ai1()

            ph, gc1, gc2, emt = self.s3.get_sample()
            wl1, wl2, wl3, wl4 = self.s4.get_sample()

            samples = [ lux,   tem,   pre,   hum,   ai1,   ai2,   ph,   gc1,   gc2,
                              emt,   wl1,   wl2,   wl3,   wl4]
            return samples
        except Exception as e:
            print("Exception " + str(f_name()) +': ' + str(e))



    # def digitize(self,p1,high_limit):
    # def calc_water_level(self,p1, p2):
    #     #    25-20L   20-10L   10-0L
    #     # p1 0        1        1
    #     # p2 0        0        1
    #     # p3 0        0        0
    #
    #     if p1
    def send_samples_to_grafana(self):
        try:
            dprint('----------------------------------------------------------------------------')
            samples = self.read_all_sensors()
            samples_names = ['lux', 'tem', 'pre', 'hum', 'ai1', 'ai2', 'ph', 'gc1', 'gc2',
                             'emt', 'wl1', 'wl2', 'wl3', 'wl4']

            write_to_influxdb('lux', samples[0])
            write_to_influxdb('tem', samples[1])
            write_to_influxdb('pre', samples[2])
            write_to_influxdb('hum', samples[3])
            write_to_influxdb('ai1', samples[4])
            write_to_influxdb('ai2', samples[5])
            write_to_influxdb('phw', samples[6])
            write_to_influxdb('gc1', samples[7])
            write_to_influxdb('gc2', samples[8])
            write_to_influxdb('emt', samples[9])
            write_to_influxdb('wl1', samples[10])
            write_to_influxdb('wl2', samples[11])
            write_to_influxdb('wl3', samples[12])
            write_to_influxdb('wl4', samples[13])

        except Exception as e:
            dprint("Exception " + str(f_name()) + ': ' + str(e))


s = HydroService()
s.start_schedule_jobs()