#!/usr/bin/python
import tkinter as Tk
import json, os, schedule, time
import threading
import utils
import grow_auto_
from functools import partial


class Application(Tk.Frame):

    led_status ='OFF'
    fan_status = 'OFF'
    pump_status = 'OFF'
    g=grow_auto_.AutoGrow()

    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)   
        self.grid()
        self.create_widgets()
        self.open_connection()

    def create_widgets(self):
        # set switches.
        self.led_switch = Tk.Button(self, text='LED '+self.led_status, command=self.led_set)
        self.led_scheduler = Tk.Button(self, text='LED SCHEDULER', command=partial(self.scheduler_thread_start, self.led_scheduler_set))
        self.led_scheduler_off = Tk.Button(self, text='LED SCHEDULER OFF', command=partial(self.scheduler_off, 'led'))

        self.fan_switch = Tk.Button(self, text='FAN '+self.fan_status, command=self.fan_set)
        self.fan_scheduler = Tk.Button(self, text='FAN SCHEDULER', command=partial(self.scheduler_thread_start, self.fan_scheduler_set))
        self.fan_scheduler_off = Tk.Button(self, text='FAN SCHEDULER OFF', command=partial(self.scheduler_off, 'fan'))

        self.pump_switch = Tk.Button(self, text='PUMP '+self.pump_status, command=self.pump_set)
        self.pump_scheduler = Tk.Button(self, text='PUMP SCHEDULER', command=partial(self.scheduler_thread_start, self.pump_scheduler_set))
        self.pump_scheduler_off = Tk.Button(self, text='PUMP SCHEDULER OFF', command=partial(self.scheduler_off, 'pump'))

        self.temperature_display = Tk.Listbox()

        # set colors.
        self.led_switch.config(fg="black", bg="red")
        self.fan_switch.config(fg="black", bg="red")
        self.pump_switch.config(fg="black", bg="red")

        # switches place.
        self.led_switch.grid(row=1, column=1)
        self.led_scheduler.grid(row=2, column=1)
        self.led_scheduler_off.grid(row=3, column=1)

        self.fan_switch.grid(row=1, column=2)
        self.fan_scheduler.grid(row=2, column=2)
        self.fan_scheduler_off.grid(row=3, column=2)

        self.pump_switch.grid(row=1, column=3)
        self.pump_scheduler.grid(row=2, column=3)
        self.pump_scheduler_off.grid(row=3, column=3)

        self.temperature_display.grid(row=3)

    # kill schedule thread.
    def scheduler_off(self, scheduler_name):
        schedule.clear(str(scheduler_name))

    # start schedule thread.
    def scheduler_thread_start(self, scheduler_name):
        thread = threading.Thread(target=scheduler_name)
        thread.start()

    def led_set(self):
        if self.led_status == 'ON':
            self.led_switch.config(fg="black", bg="red", text='LED OFF')
            self.led_status = 'OFF'
            print('LED OFF')
        else:
            self.led_switch.config(fg="black", bg="green", text='LED ON')
            self.led_status = 'ON'
            print('LED ON')

    # define when to power on led.
    def led_scheduler_set(self):
        schedule.every(2).seconds.do(self.led_set).tag('led')
        #schedule.every().day.at('18:00').do(self.led_set)
        while True:
            schedule.run_pending()
            time.sleep(1)
            # define when to power on led.

    def fan_scheduler_set(self):
        #schedule.every(5).seconds.do(self.fan_set).tag('fan')
        schedule.every().day.at('12:35').do(self.g.fan_on)
        schedule.every().day.at('12:36').do(self.g.fan_off)
        while True:
            schedule.run_pending()
            time.sleep(1)
            # define when to power on fan.

    def pump_scheduler_set(self):
        schedule.every(5).seconds.do(self.pump_set).tag('pump')
        # schedule.every().day.at('18:00').do(self.pump_set)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def fan_set(self):
        if self.fan_status == 'ON':
                if self.g.fan_off()==0:
                    self.fan_switch.config(fg="black", bg="red", text='FAN OFF')
                    self.fan_status = 'OFF'
        else:
                if self.g.fan_on()==0:
                    self.fan_switch.config(fg="black", bg="green", text='FAN ON')
                    self.fan_status = 'ON'
            
    def pump_set(self):
        if self.pump_status == 'ON':
                self.pump_switch.config(fg="black", bg="red", text='PUMP OFF')
                self.pump_status = 'OFF'
                self.g.water_off()
        else:
                self.pump_switch.config(fg="black", bg="green", text='PUMP ON')
                self.pump_status = 'ON'
                self.g.water_on()

    def open_connection(self):
        print('open')
	#g=grow_auto_.AutoGrow()

app = Application()
app.master.title('Auto Hydro System')
app.master.maxsize(10000, 10000)
app.mainloop()                            

