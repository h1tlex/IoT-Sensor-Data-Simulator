from utils import mqtt_setup, mqtt_start, connect_cloud, create_ipc_receiver
import paho.mqtt.client as mqtt

if __name__ == "__main__":
    # connect tcp server
    client_socket = create_ipc_receiver()

    # fetch data from cloud-info.json
    broker, port, username, password = connect_cloud("cloud-info.json")
    
    # connect mqtt
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="python-sensor"
    )
    mqtt_setup(client, broker, port, username, password)
    print(f"Connected to broker! Publishing sensor data...")
    client.loop_start()

    # start communication
    try:
        mqtt_start(client, client_socket, "vh001")
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()
        print("Disconnected.")

