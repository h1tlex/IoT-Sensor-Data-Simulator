import paho.mqtt.client as mqtt
import time
import random
import json

broker = "8d4064e7f56e41488e83453fdffdfc7e.s1.eu.hivemq.cloud" # HiveMQ
port = 8883
username = "fourat"
password = "Fourat2002!!!"
topic = "actia/intern/test"

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="python-sensor-simulator"
)

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("✅ Connected to MQTT Broker!")
    else:
        print(f"❌ Connection failed. Code: {reason_code}")

def on_publish(client, userdata, mid, reason_code, properties):
    print(f"📤 Published message ID: {mid}")


client.on_connect = on_connect
client.on_publish = on_publish

client.username_pw_set(username,password)
client.tls_set()
client.connect(broker,port)
client.loop_start()


print(f"Connected to broker! Sending messages to topic: {topic}")

try:
    while True:
        # random sensor data
        speed = random.randint(0, 200)
        temp = random.uniform(60.0, 110.0)
        rpm = random.randint(1000, 5000)

        sensor_data = {
            "speed" : speed,
            "temp" : temp,
            "rpm" : rpm
        }

        message = json.dumps(sensor_data)
        client.publish(topic, message)
        print(f"Sent: {sensor_data}")
        time.sleep(2)  # Send a message every 2 seconds
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
    print("\nPublisher stopped.")

