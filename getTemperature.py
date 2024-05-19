#!/home/pi/AllSkyCam/venv/bin/python
import Adafruit_DHT
import requests

#Sensortyp und GPIO festlegen
sensor = Adafruit_DHT.DHT11
gpio = 4

# Daten auslesen
url_string = 'http://influxDB.local:8086/write?db=signals'
humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
temperature = 'temperature,location=AllSky value=%f'%temperature
humidity = 'humidity,location=AllSky value=%f'%humidity

rt = requests.post(url_string, data=temperature)
rh = requests.post(url_string, data=humidity)
