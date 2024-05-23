from paho.mqtt import client as mqtt_client
import json
with open('config.json') as f:
    config = json.load(f)

client_id = config["mqtt_client_id"]
broker = config["mqtt_host"]
port = config["mqtt_port"]

if not 'client' in locals():
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    
def postData(subtopic, value):
    topic = "%s/%s"%(config["mqtt_topic"], subtopic)
    client.connect(broker, port)
    client.publish(topic, value)
    client.disconnect()
    