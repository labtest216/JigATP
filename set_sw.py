#!/usr/bin/python3
import sys
from denkovi16 import Denkovi16
from time import sleep


def user_validation(user_val, min_val, max_val):
    if str(user_val).isnumeric() is True:
        if int(user_val) < min_val or int(user_val) > max_val:
            print("max="+max_val+" val="+user_val+" min="+"min_val")
            return False
        else:
            return True
    else:
        return False

if int(len(sys.argv)) != 3:
    print("------------------ODROID-----------------")
    print("TH-VCC     1  3V3                     2  5V")
    print("TH-SDA     3  SDA1                    4  5V")
    print("TH-SCL     5  SCL1                    6  GND")
    print("           7  7                       8  TX")
    print("TH-GND     9  GND                    10  RX")
    print("           11 0                      12  1")
    print("           13 2                      14  GND")
    print("           15 3                      16  4")
    print("AI1-VDD    17 3V3                    18  5")
    print("           19 12/MOSI                20  GND")
    print("           21 13/MISO                22  6")
    print("           23 14/SCLK                24  10")
    print("AI1-GND    25 GND                    26  11")
    print("AI1-SDA    27 SDA2                   28  SCL2  AI1-SCL")
    print("           29 21                     30  GND")
    print("           31 22                     32  26")
    print("           33 23                     34  GND")
    print("           35 24                     36  27")
    print("           37 AI1                    38  1V8")
    print("           39 GND                    40  AI0\n\n")
    print("------------------SW-BOARD-----------------")
    print("sw_venta = 1\nsw_water = 2\nsw_220_v = 3\nsw_light = 4\n")
    print("sw_motor = 5\nsw____5v = 6\nsw____5v = 7\nsw____5v = 8\n")
    print("sw_fansm = 9\nsw_fanlr = 10\nsw_fanxl = 11\nsw_airpu = 12\n")
    print("sw____3v = 13\nsw____3v = 14\nsw____3v = 15\nsw___24v = 16\n\n")
    print("------------------AIx4_1-BOARD-----------------")
    print("AI1-PH")
    print("AI2-GC1")
    print("AI3-GC2")
    print("AI4-EMPTY_TRAIL\n\n")
    print("------------------AIx4_2-BOARD-----------------")
    print("AI1-WATER_LEVEL1")
    print("AI2-WATER_LEVEL2")
    print("AI3-")
    print("AI4-\n\n")
    print("------------------GET SW BOARD STATUS-----------------")
    print("  1   2   3   4  5  6  7  8    9  10  11  12 13 14 15 16")
    print("  7   6   5   4  3  2  1  0    7   6   5   4  3  2  1  0")
    print("128  64  32  16  8  4  2  1  128  64  32  16  8  4  2  1")
    print("  1   2   4   8 16 32 64 128")

else:
    rb = Denkovi16()
    sleep(0.5)
    rb.get_sw_status()
    switch = -2
    mode = -2
    while True:
        #while not user_validation(int(switch), 0, 16):
        switch = input("set switch:\nsw_venta = 1\nsw_water = 2\nsw_water_sw = 3\nsw_light = 4\nsw_motor = 5\nsw____5v = 6\nsw____5v = 7\n"
                  "sw____5v = 8\nsw_fansm = 9\nsw_fanlr = 10\nsw_fanxl = 11\nsw_airpu = 12\nsw____3v = 13\n"
                  "sw____3v = 14\nsw____3v = 15\nsw___24v = 16\n\n")
        #while not user_validation(int(switch), -1, 1):
        mode = input("set mode:\n 0/1\n\n")
        rb.set_switch(int(switch), int(mode))
        #switch = -2
        #mode = -2