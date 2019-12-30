#!/usr/bin/python3

import time
from sensor import *
from util import *
# Temperature humidity light sensor.
# I2c bus=1 I2c adr=0x4A.

class SGY39(Sensor):

	def get_sample(self):
		try:

			# Select configuration register, 0x02(02)
			# 0x40(64) Continuous mode, Integration time = 800 ms
			self._bus.write_byte_data(self._addr, 0x02, 0x40)
			time.sleep(0.5)

			# Read data back from 0x03(03), 2 bytes
			# luminance MSB, luminance LSB
			data = self._bus.read_i2c_block_data(self._addr, 0x03, 2)

			# Convert the data to lux
			exponent = (data[0] & 0xF0) >> 4
			mantissa = ((data[0] & 0x0F) << 4) | (data[1] & 0x0F)
			luminance = ((2 ** exponent) * mantissa) * 0.045

			# Output data to screen
			#dprint("Ambient Light luminance : %.2f lux" %luminance)
			return str(round(luminance))
		except Exception as e:
			dprint({str(e)})
			return


#gy39 = SGY39(1, 0x4A, 'lux')
#gy39.get_sample()

