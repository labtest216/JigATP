#!/usr/bin/python
import sys,os
from datetime import datetime
from time import sleep

import _thread
def MyThread1():
    os.system('eog /home/gb/Desktop/Mamen/1.jpeg')


def MyThread2():
    os.system('eog /home/gb/Desktop/Mamen/2.jpeg')


_thread.start_new_thread(MyThread1, ())
sleep(3)
_thread.start_new_thread(MyThread2, ())



