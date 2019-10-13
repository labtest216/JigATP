import os, sys
from pathlib import Path

project_dir = os.path.dirname(os.path.realpath(__file__))
cfg_json = str(Path.home())+'/RPi2/cfg.json'
log_dir = project_dir + '/Log/'

GrowDays = 5
FlowDays = 5