#!/usr/bin/python
import os, sys
from pathlib import Path



project_dir = os.path.dirname(os.path.realpath(__file__))
cfg_json = str(Path.home())+'/RPi2/cfg.json'
#cfg_json = '/home/odroid/RPi2/cfg.json'
log_dir = project_dir + '/Log/'


GrowDays = 45
FlowDays = 45
GrafanaDbIp = '192.168.14.17'
#GrafanaDbIp = '192.168.14.17'