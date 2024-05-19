#!/home/pi/AllSkyCam/venv/bin/python

import requests
import datetime
import pytz
import json


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


def writeInflux():
    url_string = config["influx_url"];
    
    data = getForcast();
    post_data = 'temperature,location=Weather value=%f'%data["temperature"]
    r=requests.post(url_string, data=post_data)
    
    post_data = 'dew_point,location=Weather value=%f'%data["dew_point"]
    requests.post(url_string, data=post_data)
    
    post_data = 'cloud_cover,location=Weather value=%f'%data["cloud_cover"]
    requests.post(url_string, data=post_data)
    
    post_data = 'visibility,location=Weather value=%f'%data["visibility"]
    requests.post(url_string, data=post_data)
    
    post_data = 'pressure_msl,location=Weather value=%f'%data["pressure_msl"]
    requests.post(url_string, data=post_data)
    
    post_data = 'wind_speed,location=Weather value=%f'%data["wind_speed"]
    requests.post(url_string, data=post_data)
    
    post_data = 'wind_direction, location=Weather value=%f'%data["wind_direction"]
    requests.post(url_string, data=post_data)
    
    return data


if __name__=='__main__':
    writeInflux()
    
