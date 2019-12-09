#!/usr/bin/python3
import sys
from RelayBoard.denkovi16 import Denkovi16

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
    print("       31 22                     32  26")
    print("       33 23                     34  GND")
    print("       35 24                     36  27")
    print("       37 AI1                    38  1V8")
    print("       39 GND                    40  AI0\n\n")
    print("------------------SW-BOARD-----------------")
    print("sw_venta = 1\nsw_water = 2\nsw_220_v = 3\nsw_light = 4\n")
    print("sw____5v = 5\nsw____5v = 6\nsw____5v = 7\nsw____5v = 8\n")
    print("sw_fansm = 9\nsw_fanlr = 10\nsw_fanxl = 11\nsw_airpu = 12\n")
    print("sw____3v = 13\nsw____3v = 14\nsw____3v = 15\nsw___24v = 16\n")
else:
    rb = Denkovi16()
    rb.set_switch(int(sys.argv[1]), int(sys.argv[2]))
