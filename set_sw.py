#!/usr/bin/python
import sys
from RelayBoard.denkovi16 import Denkovi16


if int(sys.argv) != 2:
    print("write ./set_sw.py sw_num sw_mode")
    print("1-2-3-4-220v\n5-6-7-8-9-12v\n")
else:
    rb = Denkovi16()
    rb.set_switch(int(sys.argv[1]), int(sys.argv[2]))
