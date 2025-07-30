from utils import mqtt_setup, mqtt_start, connect_pipe, connect_cloud
import paho.mqtt.client as mqtt
import time
import json
import os

if __name__ == "__main__":
    # connect to named pipe
    pipepath = "/tmp/can_pipe"
    connect_pipe(pipepath)

    # fetch data from cloud-info.json
    broker, port, username, password = connect_cloud("cloud-info.json")
    
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
        mqtt_start(client, pipepath, "vh001")
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()
        print("Disconnected.")

