#!/usr/bin/python
import utils
import grow_auto_
import time
g=grow_auto_.AutoGrow()
# Test buzzer.
#g.beep()
"""
# Test light.
g.led_on()
time.sleep(5)
g.led_off()
time.sleep(5)
"""
# Test water.
g.water_on()
time.sleep(5)
g.water_off()
time.sleep(5)
"""
# Test sprinkler.
g.sprinkler_on()
time.sleep(5)
g.sprinkler_off()
time.sleep(5)
# Test fan.
g.fan_on()
time.sleep(5)
g.fan_off()
"""
