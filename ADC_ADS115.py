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



class SADS115(Sensor):


    def get_sample(self):
        try:
            adc1 = Adafruit_ADS1x15.ADS1115(address=self._addr, busnum=self._bus)
            values = [0] * 4
            for i in range(4):
                # Read the specified ADC channel using the previously set gain value.
                values[i] = adc1.read_adc(i, gain=2 / 3)
                values[i] = values[i] * 0.0001875

            return values[0], values[1], values[2], values[3]
        except Exception as e:
            print(str(e))

