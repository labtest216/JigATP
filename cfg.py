# Log files.
mic_pre = '/home/odroid/Jig/log/mic.log'
mic_post = '/home/odroid/Jig/log/mic.log'

temp_stud_pre = '/home/odroid/Jig/log/temp_stud_pre.log'	
temp_stud_post = '/home/odroid/Jig/log/temp_stud_post.log'

temp_led_pre = '/home/odroid/Jig/log/temp_led_pre.log'	
temp_led_post = '/home/odroid/Jig/log/temp_led_post.log'


sol_in_pre = '/home/odroid/Jig/log/sol_in_pre.log'	
sol_in_post = '/home/odroid/Jig/log/sol_in_post.log'
				
# Pins configuration (wPi).
light_pin = 2
buzzer_pin = 2
motor_pin = 2

# Com configuration.
led_anlyzey = { 'com':'/dev/tty/ACM0', 'br':115200}
sniffer = { 'com':'/dev/ttyACM0', 'br':115200}
arduino = { 'com':'/dev/ttyACM0', 'br':9600}

# Tests limits. 
mic_test = {'limit_low':50, 'limit_high':1500}
temp_stud_test = {'limit_low':2, 'limit_high':14}
temp_leds_test = {'limit_low':2, 'limit_high':14}
rgb_led_test = {'limit_low':2, 'limit_high':14}
readsw_test = {'limit_low':0, 'limit_high':1}
mag1_test = {'limit_low':0, 'limit_high':1}
mag2_test = {'limit_low':0, 'limit_high':1}
solar_in_test = {'limit_low':0, 'limit_high':1}
solar_out_test = {'limit_low':0, 'limit_high':1}
vbat_test = {'limit_low':3.2, 'limit_high':4.6}
rssi_test = {'limit_low':3.2, 'limit_high':4.6}
per_test = {'limit_low':3.2, 'limit_high':4.6}

# Test parameters for sniffer parser log file.
RSSI = 'RSSI:'
Packet = 'Packet:'
PER = 'PER:'
Sol_IN = 'Sol_IN:'
Sol_OUT = 'Sol_OUT:'
Sol_I = 'Sol_I:'
Batt = 'Batt:'
Mic = 'Mic:'
Mag1_X = 'Mag1_X:'
Mag2_X = 'Mag2_X:'
PCBV_Temp = 'PCBV_Temp:'

