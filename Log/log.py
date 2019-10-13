import logging
import time
from config import log_path
from util import *

class Log:

    def __init__(self):
        # Create logger.
        logger = logging.getLogger("")
        logger.setLevel(logging.DEBUG)

        # Create console and file handlers and set level to debug.
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_path)

        # Create formatter.
        form = str(time.time())+'  %(asctime)s  FileName=%(filename)s  FuncName=%(funcName)s:  %(message)s'
        formatter = logging.Formatter(form)

        # Add formatter.
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # add handlers to logger
        logger.addHandler(ch)
        logger.addHandler(fh)

    def print(self):
        return logging

