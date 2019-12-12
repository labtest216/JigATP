#!/usr/bin/python3

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

    def __init__(self):
        self.rb.set_switch(sw_water, 0)

    def start_schedule_jobs(self):
        # Motor   on/off.
        schedule.every().day.at("07:00").do(self.rb.set_switch, switch_num=sw_motor, mode=1)
        schedule.every().day.at("07:01").do(self.rb.set_switch, switch_num=sw_motor, mode=0)
        # Water   on/off.
        schedule.every().day.at("07:02").do(self.rb.set_switch, switch_num=sw_water, mode=1)
        schedule.every().day.at("07:03").do(self.rb.set_switch, switch_num=sw_water, mode=0)
        schedule.every().day.at("07:05").do(self.rb.set_switch, switch_num=sw_water, mode=0)
        schedule.every().day.at("07:06").do(self.rb.set_switch, switch_num=sw_water, mode=0)

        # Light   on/off.
        # Grow:
        schedule.every().day.at("05:00").do(self.rb.set_switch, switch_num=sw_light, mode=1)
        schedule.every().day.at("23:00").do(self.rb.set_switch, switch_num=sw_light, mode=0)
        # Flow:
        #schedule.every().day.at("05:00").do(self.rb.set_switch, switch_num=sw_light, mode=1)
        #schedule.every().day.at("17:00").do(self.rb.set_switch, switch_num=sw_light, mode=0)

        # Venta   on/off.
        schedule.every().day.at("08:00").do(self.rb.set_switch, switch_num=sw_venta, mode=1)
        schedule.every().day.at("16:00").do(self.rb.set_switch, switch_num=sw_venta, mode=0)

        # AirPump on/off.
        schedule.every().day.at("08:00").do(self.rb.set_switch, switch_num=sw_venta, mode=1)
        schedule.every().day.at("09:00").do(self.rb.set_switch, switch_num=sw_venta, mode=0)

        # Sensors on/off.
        schedule.every(3).seconds.do(self.send_samples_to_grafana)

        while True:
            time.sleep(0.1)
            schedule.run_pending()



    def read_all_sensors(self):
        try:
            lux = self.s1.get_sample()
            tem, pre, hum = self.s2.get_sample()
            #ai1 = read_ai0()
            #ai2 = read_ai1()
            ph, wl1, wl2, wl3 = read_aix4_1()
            ai1, ai2, gc1, gc2 = read_aix4_2()
            samples = [lux, tem, pre, hum, ai1, ai2, gc1, gc2, wl1, wl2, wl3, ph]

            return samples
        except:
            print("Exception " + str(f_name()))

    def send_samples_to_grafana(self):
        try:
            samples = self.read_all_sensors()

            write_to_influxdb('lux', samples[0])
            write_to_influxdb('tem', samples[1])
            write_to_influxdb('pre', samples[2])
            write_to_influxdb('hum', samples[3])
            write_to_influxdb('ai1', samples[4])
            write_to_influxdb('ai2', samples[5])
            write_to_influxdb('gc1', samples[6])
            write_to_influxdb('gc2', samples[7])
            write_to_influxdb('wl1', samples[8])
            write_to_influxdb('wl2', samples[9])
            write_to_influxdb('wl3', samples[10])
            write_to_influxdb('ph', samples[11])

            dprint('--SensorsServiceOn--')
            dprint("lux, tem, pre, hum, ai1, ai2, gc1, gc2, wl1, wl2, wl3, ph")
            for sample in samples:
                dprint(str(sample))
        except:
            print('Exception ' + str(f_name()))
    def send_samples_schedule(self):
        schedule.every(3).seconds.do(self.send_samples_to_grafana)

s = HydroService()
s.start_schedule_jobs()