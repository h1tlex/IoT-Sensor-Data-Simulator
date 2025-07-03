import paho.mqtt.client as mqtt

broker = "8d4064e7f56e41488e83453fdffdfc7e.s1.eu.hivemq.cloud" # HiveMQ
port = 8883
username = "fourat"
password = "Fourat2002!!!"
topic = "actia/intern/test"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code ", rc)
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(f"Received on [{msg.topic}]: {msg.payload.decode()}")

client = mqtt.Client()
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message

client.tls_set()
client.connect(broker,port)
print(f"Connecting to broker {broker}...")
client.loop_forever()