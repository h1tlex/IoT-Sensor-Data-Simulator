import can
import json
import os

def connect_can(bus_type='socketcan', channel='can0', bitrate=500000):
    """
    Connect to a CAN bus using the specified parameters.

    :param bus_type: Type of CAN bus (default is 'socketcan').
    :param channel: CAN channel to connect to (default is 'can0').
    :param bitrate: Bitrate for the CAN connection (default is 500000).
    :return: A can.Bus instance connected to the specified CAN bus.
    """
    try:
        bus = can.Bus(channel=channel, interface=bus_type, bitrate=bitrate, receive_own_messages=True)
        print(f"Connected to {bus_type} on {channel} at {bitrate} bps.")
        return bus
    except Exception as e:
        print(f"Failed to connect to CAN bus: {e}")
        return None
    
def send_can_message(bus, message_id, data):
    """
    Send a CAN message on the connected bus.

    :param bus: The can.Bus instance to send the message on.
    :param message_id: The ID of the CAN message.
    :param data: The data payload for the CAN message.
    """
    if bus is None:
        print("Cannot send message, bus is not connected.")
        return
    
    # Ensure data is 8 bytes
    if len(data) < 8:
        data = data + [0] * (8 - len(data))
    
    msg = can.Message(arbitration_id=message_id,
                      data=data,
                      is_extended_id=False
                    )

    try:
        bus.send(msg)
        print(f"Message sent: ID={hex(message_id)}, Data={[hex(x) for x in data]}")
    except Exception as e:
        print(f"Failed to send CAN message: {e}")

def receive_can_message(bus):
    """
    Receive a CAN message from the connected bus.

    :param bus: The can.Bus instance to receive the message from.
    :return: The received can.Message or None if no message is received.
    """
    if bus is None:
        print("Cannot receive message, bus is not connected.")
        return None
    
    try:
        msg = bus.recv(timeout=2.0)  # Wait for a message for up to 2 seconds
        if msg:
            print(f"Message received: ID={hex(msg.arbitration_id)}, Data={[hex(x) for x in msg.data]}")
            return msg
        else:
            print("No message received within the timeout period.")
            return None
    except Exception as e:
        print(f"Failed to receive CAN message: {e}")
        return None
    
def decrypt_can_message(data):
    """
    Decrypt the CAN message data if necessary.

    :param data: The data payload of the CAN message.
    :return: Decrypted data.
    """
    if len(data) < 8:
        print("Data length is too short for decryption.")
        return None
    
    speed = data[0] # Speed in km/h (1 byte)
    rpm = data[1] | (data[2] << 8) # RPM (2 bytes, little-endian)
    temp = data[3]
    tension = data[4] | (data[5] << 8) # Tension (2 bytes, little-endian)
    power = data[6] | (data[7] << 8) # Power (2 bytes, little-endian)
    
    print(f"Decrypted Speed: {speed} km/h, RPM: {rpm}, Temp: {temp}°C, Tension: {tension}mV, Power: {power}W")

    return speed, rpm, temp, tension, power

def encode_can_message(rpm, tension, power):
    """
    Encode RPM, TENSION and POWER as little-endian (low byte first)

    :param rpm: RPM value.
    :param tension: Tension value in mV.
    :param power: Power value in W.
    :return: Encoded data as little-endian format.
    """
    rpm_low = rpm & 0xFF          # Get the lower 8 bits
    rpm_high = (rpm >> 8) & 0xFF  # Get the upper 8 bits

    tension_low = tension & 0xFF
    tension_high = (tension >> 8) & 0xFF

    power_low = power & 0xFF
    power_high = (power >> 8) & 0xFF

    return rpm_low, rpm_high, tension_low, tension_high, power_low, power_high


def mqtt_setup(client, broker, port, username, password):
    """
    Setup MQTT client with connection and publish callbacks.

    :param client: The MQTT client instance.
    :param broker: The MQTT broker address.
    :param port: The port to connect to the broker.
    :param username: Username for MQTT authentication.
    :param password: Password for MQTT authentication.
    """
    
    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("✅ Connected to MQTT Broker!")
        else:
            print(f"❌ Connection failed. Code: {reason_code}")

    def on_publish(client, userdata, mid, reason_code, properties):
        print(f"📤 Published message ID: {mid}\n")

    client.on_connect = on_connect
    client.on_publish = on_publish

    client.username_pw_set(username, password)
    client.tls_set()
    client.connect(broker, port)

def mqtt_start(client, pipepath="/tmp/can_pipe", vehicle_id="vh001"):
    """
    Sends data payload via mqtt to node-red dashboard.

    :param client: The MQTT client instance.
    :param pipepath: Path to the named pipe for reading CAN data.
    :param vehicle_id: Vehicle identifier for the MQTT topic (default is "vh001").
    """
    while True:
        with open(pipepath, "r") as pipe:
            line = pipe.readline()
            entry = json.loads(line.strip())
            if line:
                payload = {
                    "speed": entry["speed"],
                    "rpm": entry["rpm"],
                    "temp": entry["temp"],
                    "tension": entry["tension"],
                    "power": entry["power"]
                }

                topic = f"actia/fleet/{vehicle_id}/sensors"

                client.publish(topic, json.dumps(payload))
                print(f"Sent: {payload} to topic: {topic}")
            else:
                print("No data available.")
                break
    return
        
def can_pipe_w(msg, speed, rpm, temp, tension, power, pipepath="/tmp/can_pipe"):
    """
    Start CAN communication by sending and receiving messages.
    
    :param msg: The can.Message instance to send.
    :param speed: Speed in km/h.
    :param rpm: RPM value.
    :param temp: Temperature in °C.
    :param tension: Tension in mV.
    :param power: Power in W.
    :param pipepath: Path to the named pipe for writing CAN data (default "/tmp/can_pipe").
    """
    connect_pipe(pipepath)
    if not os.path.exists(pipepath):
        os.mkfifo(pipepath)
    
    with open(pipepath, "w") as pipe:
        data = {
                "id": hex(msg.arbitration_id),
                "speed": speed,
                "rpm": rpm,
                "temp": temp,
                "tension": tension,
                "power": power
            }
        pipe.write(json.dumps(data) + "\n")
        pipe.flush()
        print(f"Data written to pipe \n")

def connect_pipe(pipepath="/tmp/can_pipe"):
    """
     Connect to a named pipe for reading CAN data.

     :param pipepath: Path to the named pipe for reading CAN data.
    """
    if not os.path.exists(pipepath):
        os.mkfifo(pipepath)

    
def connect_cloud(cloud_info_path="cloud-info.json"):
    """
    Connect to cloud service using information from a JSON file.
    
    :param cloud_info_path: Path to the JSON file containing cloud connection info.
    :return: tuple containing broker, port, username and password.
    :raises FileNotFoundError: If the cloud info file does not exist.
    """
    if not os.path.exists(cloud_info_path):
        raise FileNotFoundError(f"Cloud info file {cloud_info_path} does not exist.")
    
    with open(cloud_info_path) as f:
        log = json.load(f)
        broker = log.get("broker")
        port = log.get("port")
        username = log.get("username")
        password = log.get("password")

    return broker, port, username, password