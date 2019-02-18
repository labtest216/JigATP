import threading
from cfg import *
from o import Odroid
from util import find_avg_value_from_file, dprint, f_name

o = Odroid()


def check_limits(limit_low, limit_high, delta):

	if delta > limit_low and delta < limit_high:
		return 0
	else:
		return -1

def print_result(post_value, pre_value, limit_low, limit_high):
	delta = post_value - pre_value
	debug_print = "post_value="+str(post_value) + " pre_value=" + str(pre_value) + " delta=" + str(delta) + " limit_low=" + str(limit_low) + " limit_high=" + str(limit_high)
	
	if check_limits(limit_low, limit_high, delta) == 0:
		dprint(f_name()+" pass "+ debug_print)
		return 0
	else:
		print(f_name() +" fail "+ debug_print)
		return -1
	

# PCBV temperature test.
def pcbv_temp(limit_low, limit_high):
	o.light_off()
	o.read_sniffer(100,temp_stud_pre)
	pre_value = find_avg_value_from_file(temp_stud_pre, PCBV_Temp)
	o.light_on()
	o.read_sniffer(100, temp_stud_post)
	o.light_off()
	post_value = find_avg_value_from_file(temp_stud_post, PCBV_Temp)

	return print_result(post_value, pre_value, limit_low, limit_high)

# PCBE temperature test, not imp on sniffer.
def pcbe_temp():
	o.read_sniffer(10,temp_leds_pre)
	pre_value = find_avg_value_from_file(temp_leds_pre, Sol_IN)
	o.set_light(5)
	o.read_sniffer(10, temp_stud_post)
	post_value = find_avg_value_from_file(temp_leds_post, Sol_IN)

	return print_result(post_value, pre_value, limit_low, limit_high)

# Solar Vin test.
def solar_in(limit_low, limit_high):
	o.light_off()
	o.read_sniffer(100, sol_in_pre)
	pre_value = find_avg_value_from_file(sol_in_pre, Sol_IN)
	o.light_on()
	o.read_sniffer(100
, sol_in_post)
	o.light_off()
	post_value = find_avg_value_from_file(sol_in_post, Sol_IN)
	
	return print_result(post_value, pre_value, limit_low, limit_high)

# Vbattery = Solar Vout test.
def Vbat():
	o.read_sniffer(10,sol_in_pre)
	pre_value = find_avg_value_from_file(sol_in_pre, Sol_IN)
	o.set_light(15)
	o.read_sniffer(10, sol_in_post)
	post_value = find_avg_value_from_file(sol_in_post, Sol_IN)
	
	return print_result(post_value, pre_value, limit_low, limit_high)

# Microphone test.
def microphone(limit_low, limit_high):
	o.buzzer_off()
	o.read_sniffer(10,mic_pre)
	pre_value = find_avg_value_from_file(mic_pre, Mic)
	o.buzzer_on()
	o.read_sniffer(10, mic_post)
	post_value = find_avg_value_from_file(mic_post, Mic)
	o.buzzer_off()

# Magnet1 test.
def microphone(limit_low, limit_high):
	o.buzzer_off()
	o.read_sniffer(10,mic_pre)
	pre_value = find_avg_value_from_file(mic_pre, Mic)
	o.buzzer_on()
	o.read_sniffer(10, mic_post)
	post_value = find_avg_value_from_file(mic_post, Mic)
	o.buzzer_off()

	return print_result(post_value, pre_value, limit_low, limit_high)

# Magnet2 test.
def microphone(limit_low, limit_high):
	o.buzzer_off()
	o.read_sniffer(10,mic_pre)
	pre_value = find_avg_value_from_file(mic_pre, Mic)
	o.buzzer_on()
	o.read_sniffer(10, mic_post)
	post_value = find_avg_value_from_file(mic_post, Mic)
	o.buzzer_off()

#RSSi  test.
def rssi(limit_low, limit_high):
	o.read_sniffer(10,mic_pre)
	pre_value = find_avg_value_from_file(mic_pre, Mic)
	o.set_light(1)
	o.read_sniffer(10, mic_post)
	post_value = find_avg_value_from_file(mic_post, Mic)

	
	return print_result(post_value, pre_value, limit_low, limit_high)

#PER  test.
def per(limit_low, limit_high):
	o.read_sniffer(10,mic_pre)
	pre_value = find_avg_value_from_file(mic_pre, Mic)
	o.set_light(1)
	o.read_sniffer(10, mic_post)
	post_value = find_avg_value_from_file(mic_post, Mic)

	
	return print_result(post_value, pre_value, limit_low, limit_high)
	

