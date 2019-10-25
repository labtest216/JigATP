#!/usr/bin/python
import os
import sys

file_service=sys.argv[1]
service=["Light","Water","Sensor"]

if sys.argv[1] == "enable":
    for i in range(0,3):
        print(os.system('cp ./Service/' +service[i] + '.service' + ' /lib/systemd/system/'))
        print(os.system('systemctl enable ' + service[i]))
        print(os.system('systemctl daemon-reload'))
        print(os.system('systemctl start ' + service[i]))
        print(os.system('systemctl unmask ' + service[i]))
elif sys.argv[1] == "disable":
    for i in range(0,3):
        print(os.system('systemctl stop ' + service[i]))
        print(os.system('systemctl mask ' + service[i]))
        print(os.system('systemctl disable ' + service[i]))
        print(os.system('systemctl daemon-reload'))
elif sys.argv[1] == "stop":
    for i in range(0,3):
        #print(str(i))
        print(os.system('systemctl stop ' + service[i]))
elif sys.argv[1] == "unmask":
    for i in range(0,3):
        print(os.system('systemctl unmask ' + service[i]))
elif sys.argv[1] == "start":
    for i in range(0,3):
        print(os.system('systemctl start ' + service[i]))

elif sys.argv[1] == "restart":
    for i in range(0, 3):
        print(os.system('systemctl restart ' + service[i]))
elif sys.argv[1] == "mask":
    for i in range(0, 3):
        print(os.system('systemctl mask ' + service[i]))
else:
    print ('Arg not valid')