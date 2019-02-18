#!/usr/bin/env python
import time
import tests
from o import Odroid
from util import find_avg_value_from_file
from cfg import *



#tests.pcbv_temp(temp_stud_test['limit_low'], temp_stud_test['limit_high'])
#tests.pcbe_temp() not imp
tests.solar_in(solar_in_test['limit_low'], solar_in_test['limit_high'])
#tests.microphone()
#tests.microphone(mic_test['limit_low'], mic_test['limit_high']
#o = Odroid()

# PCBV test.
#o.set_light(5)
#o.read_sniffer(10,'light_test.log')
#PCBV_Temp = find_avg_value_from_file(temp_stud, PCBV_Temp, PCBV_Temp_chars)
# Solar in test.

# Solar in test.
# Mic test.
#o.buzzer_on(5)
#o.read_sniffer(10,'light_test.log')
#Mic_value = find_avg_value_from_file(temp_stud, PCBV_Temp, PCBV_Temp_chars)
# Motor on.
#o.active_motor_by_arduino(20)
#o.read_sniffer(10,'light_test.log')
#Mag1 = find_avg_value_from_file(temp_stud, PCBV_Temp, PCBV_Temp_chars)
#o.speaker_on(20, 0.5)
#o.read_sniffer(10,'light_test.log')
#find_avg_value_from_file(temp_stud, PCBV_Temp)
#find_avg_value_from_file(temp_stud, PCBV_Temp, PCBV_Temp_chars)
#find_avg_value_from_file(temp_stud, PCBV_Temp, PCBV_Temp_chars)
