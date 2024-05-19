#!/usr/bin/python3
import requests
import shutil
def data():
    stat = shutil.disk_usage('.')
    return 'disk_usage,location="pi4b.local" total=%d,used=%d,free=%d'%(stat.total, stat.used, stat.free)
        
if __name__=='__main__':
    url_string = 'http://influxDB.local:8086/write?db=signals'
    r = requests.post(url_string, data=data())