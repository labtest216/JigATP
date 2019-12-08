#!/usr/bin/python
import sys
from RelayBoard.denkovi16 import Denkovi16


if int(sys.argv) != 2:
    print("write ./set_sw.py sw_num sw_mode")
    print("1-2-3-4-220v\n5-6-7-8-9-12v\n")
    print("1-venta 2-water pump 3- 4-light")
    print("9- 11-fan XL 12- air pumb")
else:
    rb = Denkovi16()
    rb.set_switch(int(sys.argv[1]), int(sys.argv[2]))
