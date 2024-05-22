#!/home/pi/AllSkyCam/venv/bin/python
import Adafruit_DHT
import requests
import weatherInfo

import RPi.GPIO as GPIO
import sys

import mqtt

import json
with open('config.json') as f:
    config = json.load(f)

target_temperature = config['target_temperature']

GPIO.setmode(GPIO.BOARD)
Signal_Pin = 16
GPIO.setup(Signal_Pin, GPIO.OUT)
print('Current heater state: ', GPIO.input(Signal_Pin))

#Sensortyp und GPIO festlegen
sensor = Adafruit_DHT.DHT11
gpio = 4

# Daten auslesen
humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)

try:
    weather = weatherInfo.getForcast()
    target_temperature = weather["dew_point"] + 5;
    if weather["temperature"] - weather["dew_point"] < 5:
        target_temperature = weather["temperature"] + 5;
    if weather['precipitation'] > 0.25:
        target_temperature = weather["temperature"] + 20;  # dry mode
except Exception as e:
    mqtt.postData('heater/error', repr(e))
    pass
    


if temperature < target_temperature:
  GPIO.output(Signal_Pin, GPIO.HIGH)
  print('New heater state: ', GPIO.input(Signal_Pin))

if temperature > target_temperature:
  GPIO.output(Signal_Pin, GPIO.LOW)
  print('New heater state: ', GPIO.input(Signal_Pin))

mqtt.postData('heater/target_temperature', target_temperature)
mqtt.postData('heater/status', GPIO.input(Signal_Pin))
mqtt.postData('DHT11/temperature', temperature)
mqtt.postData('DHT11/humidity', humidity)
