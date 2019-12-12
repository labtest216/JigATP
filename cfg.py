#!/usr/bin/python3
import os, sys
from pathlib import Path



project_dir = os.path.dirname(os.path.realpath(__file__))
print(project_dir)
cfg_json = project_dir +'/cfg.json'
log_dir = project_dir

GrowDays = 45
FlowDays = 45

sw_venta = 1
sw_water = 2
sw_220_v = 3
sw_light = 4
sw_motor = 5
sw____5v = 6
sw____5v = 7
sw____5v = 8
sw_fansm = 9
sw_fanlr = 10
sw_fanxl = 11
sw_airpu = 12
sw____3v = 13
sw____3v = 14
sw____3v = 15
sw___24v = 16


GrafanaDbIp  = '192.168.14.17'
#GrafanaDbIp = '192.168.14.17'