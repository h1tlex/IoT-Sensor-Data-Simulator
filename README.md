# IoT Sensor Data Simulator & Dashboard

This project provides a solution for simulating, collecting, and visualizing IoT sensor data from both virtual and physical CAN networks. The system connects to a CAN bus (virtual or physical), processes sensor data, and visualizes it on a real-time dashboard via MQTT and Node-RED.

## Features

- **Virtual CAN Simulation**: Simulate vehicle data without physical hardware
- **Physical CAN Integration**: Connect to real CAN networks via USB adapters
- **Real-time Dashboard**: Visualize sensor data through Node-RED
- **Cloud Integration**: Connect to MQTT brokers for cloud data streaming
- **Database Simulation**: Simulate historical sensor data for testing
- **Modular Design**: Easily extendable for different sensor types


## Prerequisites

- Python 3.8+
- Node-RED (for dashboard visualization)
- MQTT broker (local or cloud-based)
- PCAN-USB adapter (optional for physical CAN connection)

## Configure cloud connection

```json
{
  "broker": "your.mqtt.broker.com",
  "port": "your_port",
  "username": "your_username",
  "password": "your_password"
}

```

## CAN connection settings
```
Usage: python main.py <can_bus_type> ('v' for virtual, 'p' for physical)

```

**Virtual connection**:

```python

can_bus = connect_can(
        bus_type='virtual',
        channel='PCAN_VIRTUAL0',
        bitrate=500000
    )

```

**Physical connection**:

```python

can_bus = connect_can(
        bus_type='pcan',
        channel='PCAN_USBBUS1',
        bitrate=500000
    )

```