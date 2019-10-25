#!/usr/bin/python
import os
import time
from influxdb import InfluxDBClient
from datetime import datetime
from util import *
def write_to_influxdb(database,measure_name,meashure_value):
    time.sleep(0.2)
    os.system('influx -execute \''+'insert '+measure_name+' value='+meashure_value+'\' -database='+database+' -precision=rfc3339')
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
# #print(client.write(['temperature,value=250 idle=100'],{'db':'hydro'},204,'line'))