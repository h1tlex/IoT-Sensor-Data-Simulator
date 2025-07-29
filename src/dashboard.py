from utils import mqtt_setup, mqtt_start
import paho.mqtt.client as mqtt
import time
import json
import os

pipepath = "/tmp/can_pipe"
if not os.path.exists(pipepath):
    raise FileNotFoundError(f"Pipe path {pipepath} does not exist.")

if __name__ == "__main__":
    # fetch data from cloud-info.json
    with open("cloud-info.json") as log_file:
        log = json.load(log_file)
        broker = log.get("broker")
        port = log.get("port")
        username = log.get("username")
        password = log.get("password")
    
    # connect mqtt
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="python-sensor"
    )
    mqtt_setup(client, broker, port, username, password)
    print(f"Connected to broker! Publishing sensor data every 2 seconds...")
    client.loop_start()

    # start communication
    try:
        mqtt_start(client, pipepath,"vh001")
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()
        print("Disconnected.")

