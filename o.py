#!/usr/bin/env python
import time
import sys
from serial import Serial
import wiringpi as wpi
from cfg import *

class Odroid:

	
        def __init__(self):
            self.init_board()
	    print("init end")

        def init_board(self):
	    print("init board")
            wpi.wiringPiSetup()
	    # Output pins.
            wpi.pinMode(light_pin, 1)
            wpi.pinMode(buzzer_pin, 1)
            wpi.pinMode(motor_pin, 1)
	    # Input pins.
	



        def motor_on(self, t):
                print("not imp")

        def light_on_time(self, t):
		print("light on")
                wpi.digitalWrite(light_pin, 1)
                time.sleep(t)
                wpi.digitalWrite(light_pin, 0)
                print("light off")

	def light_on(self):
                wpi.digitalWrite(light_pin, 1)
		print("light on")

	def light_off(self):
                wpi.digitalWrite(light_pin, 0)
		print("light off")

	def buzzer_on_time(self, t):
		print("buzzer on")
                wpi.digitalWrite(buzzer_pin, 1)
                time.sleep(t)
                wpi.digitalWrite(buzzer_pin, 0)
                print("buzzer off")
	
	def buzzer_on(self):
		time.sleep(1)
		print("buzzer on")
                wpi.digitalWrite(buzzer_pin, 1)
               
	def buzzer_off(self):
		time.sleep(1)
		print("buzzer off")
                print(str(wpi.digitalWrite(buzzer_pin, 0)))

        def buzzer_on_pwm(self, t, duty_cycle):
		on_time = duty_cycle
		off_time = 1-duty_cycle
		sec = 0
		while sec<t:
			print("buzzer on")
		        wpi.digitalWrite(buzzer_pin, 1)
		        time.sleep(on_time)
		        wpi.digitalWrite(buzzer_pin, 0)
			time.sleep(off_time)
		        print("buzzer off")
			sec+=1

        def read_sniffer(self, lines, file_path):
	    f = open(file_path, 'w+')
	    f.truncate()
            com = Serial(sniffer['com'], sniffer['br'], 8, 'N', 1)
            if com.is_open:
                print("Communication with sniffer open.")
		i = 0
                while i<lines :
                    data = com.readline()
		    f.write(data)
                    print(data)
		    i+=1
		f.close()
		com.close()
		print("Communication with sniffer close.")
            else:
                print("Com can not open, Communication with sniffer fail.")

	
        def active_motor_by_arduino(self):
            com = Serial(arduino_com, 9600, 8, 'N', 1)
            if com.is_open:
                print("Communication with sniffer open.")
                while True:
                    data = com.read()
                    print(data)
            else:
                self.dprint("Com can not open, Communication with sniffer fail.")

