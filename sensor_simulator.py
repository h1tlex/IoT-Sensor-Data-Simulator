import paho.mqtt.client as mqtt
import time
import random
import json
import sqlite3

DB_PATH = 'sensor_data.db'

def connect_db():
    """Fetch records in sequence from the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get total records
    cursor.execute("SELECT COUNT(*) FROM sensor_readings")
    total_records = cursor.fetchone()[0]
    
    # Initialize position tracker in flow context
    if not flow.get("current_position"):
        flow["current_position"] = 0

    current_position = flow.get("current_position")
    
    # Fetch next record
    cursor.execute("SELECT * FROM sensor_readings LIMIT 1 OFFSET ?", (current_position,))
    record = cursor.fetchone()
    
    if record:
        # Move to next position
        new_position = (current_position + 1) % total_records  # Loop back to start
        flow["current_position"] = new_position

        # Map record to data structure
        return {
            "id": record[0],
            "timestamp": record[1],
            "speed": record[2],
            "rpm": record[3],
            "temp": record[4],
            "tension": record[5],
            "power": record[6]
        }
    return None

vehicles = [
    {"id": "vh001", "type": "bus"},
    {"id": "vh002", "type": "truck"},
    {"id": "vh003", "type": "car"}
]


broker = "8d4064e7f56e41488e83453fdffdfc7e.s1.eu.hivemq.cloud" # HiveMQ
port = 8883
username = "fourat"
password = "Fourat2002!!!"

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

flow = {"current_position": 0}


print(f"Connected to broker! Publishing sensor data every 2 seconds...")

try:
    while True:
        for vehicle in vehicles:
            print(f"Processing vehicle: {vehicle['id']} ({vehicle['type']})")
            sensor_data = connect_db()

            if sensor_data:
                payload = {
                    "speed": sensor_data["speed"],
                    "rpm": sensor_data["rpm"],
                    "temp": sensor_data["temp"],
                    "tension": sensor_data["tension"],
                    "power" : sensor_data["power"]
                }

                topic = f"actia/fleet/{vehicle['id']}/sensors"

                client.publish(topic, json.dumps(payload))
                print(f"Sent: {payload} to topic: {topic}")
            else:
                print("No sensor data available in the database.")
                
        time.sleep(2)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
    print("\nPublisher stopped.")

