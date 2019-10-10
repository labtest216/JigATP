# ---------------Sniffer---------------.
snif_flag = 1
snif_com = "com15"
snif_br = 115200
# ---------------Getway---------------.
gw_flag = 1
gw_com = 1
gw_br = 9600
# ---------------RelyBoard---------------.
rb_flag = 1
rb_com = "com14"
rb_br = 9600
# Relay numbers.
light1 = 1
light2 = 2
buzzer = 3
pneumatic = 4
lda = 5
fan = 6
sniffer = 7
getway = 8
motor = 9
# ---------------Temperature sensor---------------.
I2c_bus = 2
Addr = "0x45"
# ---------------Led sensor---------------.
lda_com = "com17"
lda_br = 115200
# ---------------Motor---------------.
m_flag = 1
m_com = "com14"
m_br = 9600
# Motor commands and ack.
start = "start_motor"
start_ok = "Start_Motor_OK"
stop = "stop_motor"
stop_ok = "Stop_Motor_OK"
speed = "set_speed_"
speed_ok = "Set_Speed_OK"
pdir = "pos_MotorDirction"
ndir = "neg_MotorDirction"
invert_dir = "invert_MotorDirction"
dir_ok = "Set_MotorDir_OK"
# ---------------Speaker---------------.
sound_file = "CarSound.wav"
# ---------------Data base---------------.
connection = "mongodb://localhost:27017/"
db = "test_reports"
col = "test_report"
# ---------------Log files---------------.
log_path = "D:\\Projects\\JigATP\\Jig\\log\\log.txt"


# ---------------Test Params---------------.
class PcbvTempTestParams:
    limit_low = 1
    limit_high = 6
    result_unit = "C"
    sniffer_parser = "PCBV_Temp:"
    sniffer_lines = 10


class PcbeTempTestParams:
    limit_low = 1
    limit_high = 6
    result_unit = "C"
    sniffer_parser = "PCBV_Temp:"
    sniffer_lines = 100

class MicTestParams:
    limit_low = 50
    limit_high = 1500
    sniffer_parser = "Mic"
    sniffer_lines = 100




# Tests limits.
mic_test = {'limit_low': 50, 'limit_high': 1500}
temp_stud_test = {'limit_low': 2, 'limit_high': 14}
temp_leds_test = {'limit_low': 2, 'limit_high': 14}
rgb_led_test = {'limit_low': 2, 'limit_high': 14}
readsw_test = {'limit_low': 0, 'limit_high': 1}
mag1_test = {'limit_low': 0, 'limit_high': 1}
mag2_test = {'limit_low': 0, 'limit_high': 1}
solar_in_test = {'limit_low': 0, 'limit_high': 1}
solar_out_test = {'limit_low': 0, 'limit_high': 1}
vbat_test = {'limit_low': 3.2, 'limit_high': 4.6}
rssi_test = {'limit_low': 3.2, 'limit_high': 4.6}
per_test = {'limit_low': 3.2, 'limit_high': 4.6}

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

