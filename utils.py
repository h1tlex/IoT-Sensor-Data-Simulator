import can

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
        return None, None
    
    speed = data[0] # Speed in km/h (1 byte)
    rpm = data[1] | (data[2] << 8) # RPM (2 bytes, little-endian)
    
    return speed, rpm