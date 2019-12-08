#!/usr/bin/python
import os
import time
from influxdb import InfluxDBClient
from datetime import datetime
from util import *


def write_to_influxdb(measure_name, meashure_value):
    ip_local = get_my_ip()
    ip_remote = '192.168.14.17'
    host = 'influx -host ' + str(ip_remote) + ' -execute '
    cmd = '\'insert ' + measure_name + ' value=' + meashure_value
    db = '\' -database=\'hydro\''
    time = ' -precision=\'rfc3339\''
    command = host + cmd + db + time
    print(command)

    command_local = 'influx -execute \'' + 'insert ' + measure_name + \
                    ' value='+meashure_value+'\' -database=\'+database+\' -precision=rfc3339'
    dprint(command)
    os.system(command)

    return 0
# data = [
#     {
#         "measurement": "temperature",
#         "time": int(time.time()),
#         "fields": {
#             "value": 45
#
#         }
#     }
#         ]
#
#
#
#
# client = InfluxDBClient(host='localhost', port=8086, username='admin', password='qweasdzxc', database='hydro')
# client.switch_database('hydro')
#
# print(client.write_points(data, time_precision='rfc3339', protocol='json'))
# #print(client.write(['temperature,value=250 idle=100'],{'db':'hydro'},204,'line') )

#print(write_to_influxdb('lux','1002'))