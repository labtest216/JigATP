from cfg import * 
import smtplib, socket, time, os, signal, json, sys
import traceback
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import inspect


def find_avg_value_from_file(file_path, value,):
	f = open(file_path, 'r')
	lines = f.readlines()

	print('value to find=' + value)
	avg_value = 0
	for line in lines:
		lines_split = line.split(',')
		v = find_value_in_line(lines_split, value)
		#print(v)
		avg_value += float(v[len(value):])
	avg_value /=  len(lines)
	print('avg '+value+'='+str(avg_value))
	return avg_value

		
	
	
def find_value_in_line(lines, value):
	for line in lines:
		if line.find(value) != -1:
			return line

# Debug printer.
def dprint(data_to_print):
    # os.system('echo ' + str(time()) + ' ' + str(data_to_print))
    print(str(time.time()) + " " + str(datetime.now()) + " " + data_to_print)


# Get function name.
def f_name():
    stack=traceback.extract_stack()
    filename, codeline, funcName, text = stack[-3]
    return funcName

# Get function name.
def f_name_():
    stack=traceback.extract_stack()
    filename, codeline, funcName, text = stack[-1]
    return funcName

