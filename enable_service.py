#!/usr/bin/python
import os
import sys

file_service=sys.argv[1]
if sys.argv[1] != None:
    # Init service.
    print(os.system('cp ./' + file_service + ' /lib/systemd/system/'))
    print(os.system('systemctl enable ' + file_service))
    print(os.system('systemctl daemon-reload'))
    print(os.system('systemctl start ' + file_service))
else:
    print ('Enter arg file.service')