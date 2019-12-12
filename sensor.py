#!/usr/bin/python

import smbus
import time


class Sensor:

	def __init__(self, i2c_bus, address, unit):
		# Get I2C bus number address and unit.
		self._unit = unit
		self._addr = address
		self._bus = smbus.SMBus(i2c_bus)

		def get_sample(self): pass
