
import smtplib, socket, time, os, signal, json, sys, logging
import traceback
from setuptools import setup
from datetime import datetime
import pyglet



def find_avg_value_from_file(file_path, value):
	f = open(file_path, 'r')
	lines = f.readlines()

	print('value to find=' + value)
	avg_value = 0
	for line in lines:
		lines_split = line.split(',')
		v = find_value_in_line(lines_split, value)
		print(v)
		avg_value += float(v[len(value):])
	avg_value /= len(lines)
	print('avg '+value+'='+str(avg_value))
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
	print(str(time.time()) + " " + str(datetime.now()) + " " + data_to_print)


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
