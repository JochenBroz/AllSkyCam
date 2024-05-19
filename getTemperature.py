#!/home/pi/AllSkyCam/venv/bin/python
import Adafruit_DHT
import requests

import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BOARD)
Signal_Pin = 16
GPIO.setup(Signal_Pin, GPIO.OUT)
print('Current heater state: ', GPIO.input(Signal_Pin))

#Sensortyp und GPIO festlegen
sensor = Adafruit_DHT.DHT11
gpio = 4

# Daten auslesen
url_string = 'http://influxDB.local:8086/write?db=signals'
humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)

if temperature <30:
  GPIO.output(Signal_Pin, GPIO.HIGH)
  print('New heater state: ', GPIO.input(Signal_Pin))

if temperature >= 30:
  GPIO.output(Signal_Pin, GPIO.LOW)
  print('New heater state: ', GPIO.input(Signal_Pin))


# Write Temperature to Influx
temperature = 'temperature,location=AllSky value=%f'%temperature
humidity = 'humidity,location=AllSky value=%f'%humidity

rt = requests.post(url_string, data=temperature)
rh = requests.post(url_string, data=humidity)

