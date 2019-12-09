#!/usr/bin/python3
from serial import Serial
import serial.tools.list_ports
from util import *
from RelayBoard.denkovi16 import Denkovi16

def get_my_com():

    list = {}
    

    comlist = serial.tools.list_ports.comports()
    connected_com = []
    for element in comlist:
        print(str(element))
        connected_com.append(element.device)
    print("Connected COM ports: " + str(connected_com))

def get_com1(self):
    try:
        comlist = serial.tools.list_ports.comports()
        connected_com = []
        for element in comlist:
            connected_com.append(element.device)
        print("Connected COM ports: " + str(connected_com))

        for com in connected_com:
            if self.init_com(self._com, self._br) == 0:  # Try init com.
                if self.init_board() == 0:  # Try test com.
                    print(self.get_class_name() + " :" + str(com))
                    self._com.name = str(com)
                    self._com.close()
                    return str(com)
                else:
                    print('fail')
                    return -1
            else:  # Try next com.
                self._com.close()
    except Exception as e:
        print(e)


get_my_com()
