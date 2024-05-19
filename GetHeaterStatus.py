#!/usr/bin/python3
import requests
import RPi.GPIO as GPIO
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
Signal_Pin = 16
GPIO.setup(Signal_Pin, GPIO.OUT)


def data():
    stat = GPIO.input(Signal_Pin)
    return 'heater,location=AllSky status=%d'%GPIO.input(Signal_Pin)
        
if __name__=='__main__':
    url_string = 'http://influxDB.local:8086/write?db=signals'
    r = requests.post(url_string, data=data())
