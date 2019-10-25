#!/usr/bin/python3
import smbus
import time

# SHT31D default address.
SHT31_I2CADDR = 0x45

# PWD & AI.
_pwm_dir = '/sys/devices/platform/pwm-ctrl/'
_ani0_dir = '/sys/class/saradc/saradc_ch0'
_ani1_dir = '/sys/class/saradc/saradc_ch1'


def init_gpio():
    try:
        # Init digital input pins.
        wpi.wiringPiSetup()
        wpi.pinMode(self._door_left, 0)
        wpi.pinMode(self._door_right, 0)
        wpi.pinMode(self._sw0, 0)
        wpi.pinMode(self._sw1, 0)

        # Init digital output pins.
        wpi.pinMode(self._ph0, 1)
        wpi.digitalWrite(self._ph0, 1)  # Motor 0 dir with clk.
        wpi.pinMode(self._led0, 1)
        wpi.digitalWrite(self._led0, 1)  # Motor 0 led off.
        wpi.pinMode(self._ph1, 1)
        wpi.digitalWrite(self._led1, 1)  # Motor 1 dir with clk.
        wpi.pinMode(self._led1, 1)
        wpi.digitalWrite(self._led1, 1)  # Motor 1 led off.
    except Exception as e:
        self.debug_print(e)


def read_ai0():
    try:
        with open('/sys/class/saradc/saradc_ch0', 'r') as file:
            ai0 = file.readline()
        #	self.dprint('ai0='+str(ai0))
        return str(int(ai0))

    except Exception as e:
        print(str(e))


def read_ai1():
    try:
        with open('/sys/class/saradc/saradc_ch1', 'r') as file:
            ai1 = file.readline()
        #	self.dprint('ai1=' + str(ai1))
        return str(int(ai1))
    except Exception as e:
        print(str(e))

def set_pwm0(dutyc):
    # Set led off/on.
    if int(dutyc) < 10:
        wpi.digitalWrite(self._led0, 1)
    else:
        wpi.digitalWrite(self._led0, 0)

    cmd = 'echo ' + str(dutyc) + ' > ' + self._pwm_dir + 'duty0'
    # self.dprint('cmd='+str(cmd))
    # self.dprint('dutyc='+str(dutyc))
    os.system(str(cmd))


def set_pwm1(dutyc):
    # Set led off/on.
    if int(dutyc) < 10:
        wpi.digitalWrite(self._led1, 1)
    else:
        wpi.digitalWrite(self._led1, 0)

    cmd = 'echo ' + str(dutyc) + ' > ' + self._pwm_dir + 'duty1'
    # self.dprint('cmd='+str(cmd))
    # self.dprint('dutyc='+str(dutyc))
    os.system(str(cmd))


def enable_pwm(self):
    os.system('sudo modprobe pwm-meson npwm=2')
    os.system('sudo modprobe pwm-ctrl')
    os.system('echo 0 > ' + self._pwm_dir + 'duty0')
    os.system('echo 0 > ' + self._pwm_dir + 'duty1')
    os.system('echo 1 > ' + self._pwm_dir + 'enable0')
    os.system('echo 1 > ' + self._pwm_dir + 'enable1')
    os.system('echo 100000 > ' + self._pwm_dir + 'freq0')
    os.system('echo 100000 > ' + self._pwm_dir + 'freq1')


def disable_pwm(self):
    os.system('echo 0 > ' + self._pwm_dir + 'duty0')
    os.system('echo 0 > ' + self._pwm_dir + 'duty1')
    os.system('echo 0 > ' + self._pwm_dir + 'enable0')
    os.system('echo 0 > ' + self._pwm_dir + 'enable1')
    os.system('sudo modprobe -r pwm-ctrl')
    os.system('sudo modprobe -r pwm-meson')



