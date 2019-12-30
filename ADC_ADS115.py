#!/usr/bin/python3
# Simple demo of continuous ADC conversion mode for channel 0 of the ADS1x15 ADC
# with the comparator enabled.
# Author: Tony DiCola
# License: Public Domain

# gain=2/3 step=187.5[uv] bits=-32768 to +32767 scale=+-6.144[v]
# Vdigital*0.0001875=Vanalog
import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15
from util import *
from sensor import *



class SADS115():
    def __init__(self, busnum, address, unit):
        print(str(address)+' ' +str(busnum))
        self.adc1 = Adafruit_ADS1x15.ADS1115(address=address, busnum=busnum)
        self.unit = unit

    def get_sample(self):
        try:
            values = [0] * 4
            for i in range(4):
                # Read the specified ADC channel using the previously set gain value.
                values[i] = self.adc1.read_adc(i, gain=2 / 3)
                values[i] = values[i] * 0.0001875

            return str(values[0]), str(values[1]), str(values[2]), str(values[3])
        except Exception as e:
            print(str(e))

