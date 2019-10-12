#!/usr/bin/python3
from serial import Serial
import serial.tools.list_ports

from RelayBoard.denkovi16 import Denkovi16

def get_my_com():

    list = {}
    

    comlist = serial.tools.list_ports.comports()
    connected_com = []
    for element in comlist:
        connected_com.append(element.device)
    print("Connected COM ports: " + str(connected_com))

    for dev in devs:
        for com in connected_com:
            if dev.get_com(com) == 0:
                print(dev.get_class_name() + " com:" + str(com))
                list.update(dev.get_class_name(), str(com))
                return str(com)




get_my_com()
