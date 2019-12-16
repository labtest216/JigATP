#!/usr/bin/python

from datetime import datetime
import socket
import os
import psutil
import json
import time
import traceback

from subprocess import Popen, PIPE
import pyglet
from cfg import *




def write_to_influxdb(measure_name, meashure_value):
    ip_local = get_my_ip()
    ip_remote = '192.168.14.17'
    host = 'influx -host ' + str(ip_remote) + ' -execute '
    cmd = '\'insert ' + measure_name + ' value=' + meashure_value
    db = '\' -database=\'hydro\''
    time_format = ' -precision=\'rfc3339\''
    command = host + cmd + db + time_format
    dprint(command)

    command_local = 'influx -execute \'' + 'insert ' + measure_name + \
                    ' value='+meashure_value+'\' -database=\'+database+\' -precision=rfc3339'
    dprint(command)
    os.system(command)

    return 0

def find_avg_value_from_file(file_path, value):
    f = open(file_path, 'r')
    lines = f.readlines()

    dprint('value to find=' + value)
    avg_value = 0
    for line in lines:
        lines_split = line.split(',')
        v = find_value_in_line(lines_split, value)
        dprint(v)
        avg_value += float(v[len(value):])
    avg_value /= len(lines)
    dprint('avg ' + value + '=' + str(avg_value))
    return avg_value


def check_limits(limit_low, limit_high, delta):
    if limit_low <= delta <= limit_high:
        return 0
    else:
        return -1


def find_value_in_line(lines, value):
    for line in lines:
        if line.find(value) != -1:
            return line


# Debug printer.
def dprint(data_to_print):
    with open(project_dir+str('/Sys.log'), 'a+') as file:
        file.write(str(datetime.now()) + " " + data_to_print+"\n")
    print(str(datetime.now()) + " " + data_to_print + "\n")


# Get function name.
# -2=current frame, -3=up frame.
def f_name(level=None):
    stack = traceback.extract_stack()
    if level is None:
        file_name, code_line, func_name, text = stack[-2]
    else:
        file_name, code_line, func_name, text = stack[level]
    return func_name


# Play sound file.
def play_file(sound_file, seconds_to_play):
    # Edit pyglet.app.run for stop playing wave file.
    player = pyglet.media.Player()
    music = pyglet.media.load(sound_file)
    player.queue(music)
    player.play()
    pyglet.app.run(seconds_to_play)


# Create object on run time by reflection (class name = "import_file.class_name".
def get_class(class_name):
    parts = class_name.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


# Get or set parameters in json file.
def config_file(cfg_file, key, value):
    json_file = open(cfg_file, "r+")
    data = json.load(json_file)
    try:
        if value == 'get':  # Get value.
            return str(data[str(key)])
        else:  # Set value.
            data[str(key)] = value
            json_file.seek(0)  # rewind
            json.dump(data, json_file, sort_keys=True, indent=4)
            json_file.truncate()
    except Exception as e:
        dprint(str(e))

def get_my_ip():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    my_ip = s.getsockname()[0]
    s.close()
    return str(my_ip)

def check_ping(ip_address):
    p = Popen(["ping", ip_address], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    res = p.communicate(timeout=30)[0].decode(errors='ignore')
    dprint("response= " + str(res))
    if "(0% loss)" in res:
        print(ip_address + "is responding to pings")
        return True
    else:
        dprint(ip_address + " missed pings")
        return False
