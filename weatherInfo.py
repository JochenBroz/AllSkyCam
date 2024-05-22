#!/home/pi/AllSkyCam/venv/bin/python
import requests
import datetime
import pytz
import json
import mqtt


with open('config.json') as f:
    config = json.load(f)
    

def getForcast():
    # Hourely Waether Data
    url = "https://api.brightsky.dev/weather";
    n = datetime.datetime.now(pytz.timezone( config["time_zone"] )).isoformat()
    
    querystring = {
        "date":n,
        "dwd_station_id":config["dwd_station_id"]
    }
    
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()['weather'][0]


def writeMQTT():
    url_string = config["influx_url"];
    
    data = getForcast();
    mqtt.postData('weather/precipitation',data['precipitation']);
    mqtt.postData('weather/pressure_msl',data['pressure_msl']);
    mqtt.postData('weather/sunshine',data['sunshine']);
    mqtt.postData('weather/temperature',data['temperature']);
    mqtt.postData('weather/wind_direction',data['wind_direction']);
    mqtt.postData('weather/wind_speed',data['wind_speed']);
    mqtt.postData('weather/cloud_cover',data['cloud_cover']);
    mqtt.postData('weather/dew_point',data['dew_point']);
    mqtt.postData('weather/visibility',data['visibility']);
    mqtt.postData('weather/wind_gust_speed',data['wind_gust_speed']);
    return data


if __name__=='__main__':
    writeMQTT()
    
