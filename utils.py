#!/usr/bin/python

import datetime
import traceback

def f_name():
	stack=traceback.extract_stack()
	filename, codeline, funcName, text = stack[-2]
	return funcName

def dprint(data_to_print):
    print(str(datetime.datetime.now()) +" "+ str(data_to_print)+".")