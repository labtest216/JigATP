#!/usr/bin/python3
from Loggers import *
import psutil, json, logging, time
import traceback
import pyglet
import re
from paramiko import SSHClient, AutoAddPolicy
from threading import Thread
import queue
from subprocess import Popen, PIPE
from playsound import playsound
import threading

def init_logger(class_name):
	# Create logger.
	logger = logging.getLogger(class_name)
	logger.setLevel(logging.DEBUG)

	# Create console and file handlers and set level to debug.
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	fh = logging.FileHandler("/home/Hydro.log")

	# Create formatter.
	form = str(time.time()) + '  %(asctime)s  FileName=%(filename)s  FuncName=%(funcName)s:  %(message)s'
	formatter = logging.Formatter(form)

	# Add formatter.
	ch.setFormatter(formatter)
	fh.setFormatter(formatter)

	# add handlers to logger
	logger.addHandler(ch)
	logger.addHandler(fh)
	return logger

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
        print(f"Can not set or get value on cfg file. Exception message: {str(e)} + {sys.exc_info()}")


def kill_all_open_serial_proccesses():
    print("Killing opened serial and ssh processes")
    processes_to_kill = ["javaw","docklight"]
    try:
        for process_to_kill in processes_to_kill:
            processes = psutil.process_iter(attrs=None, ad_value=None)
            for process in processes:
                current_process = process.name().lower()
                if process_to_kill in current_process:
                    print(f"Killed {current_process} process")
                    process.kill()
        print("Finish killing of opened serial and ssh processes")
    except Exception as e:
        print(f"Failed to kill all serial and ssh processes. Exception message: {str(e)} + {sys.exc_info()}")


def copy_file_to_ssh(remote_ip_address, password, source_location, dest_location, username=SETUP["user"], cert=''):
    print(f"Copying {source_location} to {dest_location} on {remote_ip_address}")
    try:
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        if cert == '':
            ssh.connect(remote_ip_address, username=username, password=password)
        else:
            ssh.connect(remote_ip_address, username=username, key_filename=cert)
        sftp = ssh.open_sftp()
        sftp.put(source_location, dest_location)
        sftp.close()
        ssh.close()
        print(f"Finish copying {source_location} to {dest_location} on {remote_ip_address}")
    except Exception as e:
        print(f"Failed to copy {source_location} to {dest_location} on {remote_ip_address}. Exception message: {str(e)} + {sys.exc_info()}")


def copy_file_from_ssh(remote_ip_address, password, source_location, dest_location, username=SETUP["user"], cert=''):
    print(f"Copying {source_location} from {remote_ip_address} to {dest_location}")
    try:
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        if cert == '':
            ssh.connect(remote_ip_address, username=username, password=password)
        else:
            ssh.connect(remote_ip_address, username=username, key_filename=cert)
        sftp = ssh.open_sftp()
        sftp.get(source_location, dest_location)
        sftp.close()
        ssh.close()
        print(f"Finish copying {source_location} from {remote_ip_address} to {dest_location}")
    except Exception as e:
        print(f"Failed to copy {source_location} from {remote_ip_address} to {dest_location}. Exception message: {str(e)} + {sys.exc_info()}")


def exec_ssh_command(remote_ip_address, password, command, username=SETUP["user"], cert=''):
    print(f"Executing {command} on {remote_ip_address}")
    try:
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        if cert == '':
            ssh.connect(remote_ip_address, username=username, password=password)
        else:
            ssh.connect(remote_ip_address, username=username, key_filename=cert)
        stdin, stdout, stderr = ssh.exec_command(command)
        output = str(stdout.read())
        ssh.close()
        print(f"Successfully executed {command} on {remote_ip_address}")
        time.sleep(1)
    except Exception as e:
        print(f"Failed to execute {command} on {remote_ip_address}. Exception message: {str(e)} + {sys.exc_info()}")
        return ''
    return output

#Function return True if filename exist in path at remote_ip_address or False if it doesn't
def check_if_file_exist_remote_ssh(remote_ip_address, username, password, path, filename):
    print(f"Checking if {filename} exists in {path} on {remote_ip_address}")
    try:
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(remote_ip_address, username=username, password=password)
        sftp = ssh.open_sftp()
        print(f'Remote path: {path}/{filename}')
        try:
            sftp.stat(path + "/" + filename)
        except IOError as ex:
            if 'No such file' in str(ex):
                print(f"{filename} doesn't exists in {path} on {remote_ip_address}")
                ssh.close()
                return False
        # stdin, stdout, stderr = ssh.exec_command(command)
        # output = str(stdout.read())
        print(f"{filename} exists in {path} on {remote_ip_address}")
        ssh.close()
        # print(f"Successfully executed {command} on {remote_ip_address}")
    except Exception as e:
        print(f"Failed to check if {filename} exists in {path} on {remote_ip_address}. Exception message: {str(e)} + {sys.exc_info()}")
    return True



def check_ping(ip_address):
    p = Popen(["ping", ip_address],stdin=PIPE, stdout=PIPE, stderr=PIPE)
    res = p.communicate(timeout=30)[0].decode(errors='ignore')
    print(f"response = {res}")
    if "(0% loss)" in res:
        print(f"{ip_address} is responding to pings")
        return True
    else:
        print(f"{ip_address} missed pings")
        return False

