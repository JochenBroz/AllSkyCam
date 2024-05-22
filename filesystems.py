#!/usr/bin/python3
import mqtt
import shutil
from gpiozero import CPUTemperature

stat = shutil.disk_usage('.')

mqtt.postData('disk/totat', stat.total)
mqtt.postData('disk/used', stat.used)
mqtt.postData('disk/free', stat.free)
mqtt.postData('cpu/temperature', CPUTemperature().temperature)
        
