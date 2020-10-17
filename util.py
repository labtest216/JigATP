#!/usr/bin/python3

from datetime import datetime
import socket
import os
import psutil
import json
import time
import traceback

import cv2
from influxdb import InfluxDBClient
from subprocess import Popen, PIPE
import pyglet

from cfg import *





def get_frame_from_camera(out_path, picture_name=''):
    try:
        # Get connected cameras.
        os.system('ls /dev/video* > /tmp/ls_dev.log')
        with open('/tmp/ls_dev.log', 'r') as log_file:
            lines = log_file.readlines()
        print(lines)

        i = 0
        cameras = []
        while i < len(lines):
            cap = cv2.VideoCapture(i)
            if not cap.read()[0]:
                print('')
            else:
                cameras.append(i)
                print(f"Find camera {i}.")
            cap.release()
            i += 1

        print("taking 4 pictures of stud")
        cap = cv2.VideoCapture(cameras[1])
        framerate = cap.get(cv2.CAP_PROP_FPS)/3
        framecount = 0
        number_of_snapshot=0
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        print("checking if camera is connected")
        if cap.isOpened():
            print("camera is connected")
            ret, frame = cap.read()
        else:
            print("camera isn't connected")
            ret=False
        print("starting live video from camera")
        while ret:
            ret, frame = cap.read()
            if framecount == 0:
                time.sleep(2)
            framecount += 1
            if number_of_snapshot < 4:
                if framecount % framerate == 0 and framecount != 1:
                    number_of_snapshot += 1
                    current_time = datetime.now().replace(microsecond=0)
                    text = 'taken: ' + str(current_time)  # create time stamp for image
                    cv2.putText(frame, text, (10, 60), font, 1, (0, 255, 0), 1)
                    text2 = str(picture_name)
                    cv2.putText(frame, text2, (10, 30), font, 1, (0, 255, 0), 1)
                    print(f"taking snapshot out of live video, snapshot number: {number_of_snapshot}")
                    cv2.imwrite(os.path.join(out_path, f"{current_time}_{picture_name}--.png"), frame)
            else:
                print("done taking 4 snapshots out of live video from the camera")
                break
        print("release camera process")
        cap.release()
        last_pic_dir = os.path.join(out_path, str(picture_name) + "picture_number" + str(4) + '.png')
        return last_pic_dir
    except Exception as e:
        print(f"Failed to take snapshot from camera. Exception message: {str(e)}")
        return False
get_frame_from_camera("/home/gb","10-5-2020")
def write_to_influxdb(measure_name, test_status):
    db_name ='hydro'
    db_ip = '192.168.14.17'
    client = InfluxDBClient(db_ip, database=db_name)
    json_body = [
        {
            "measurement": measure_name,  # test_status
            "fields": {
                "value": float(test_status)
            }
        }
    ]
    client.write_points(json_body)
    dprint('Influxdb: db_name=' + db_name + ' measure_name=' + measure_name + ' test_status=' + test_status)
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
