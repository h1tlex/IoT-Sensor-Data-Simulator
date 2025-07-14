# IoT Sensor Dashboard
Simulate vehicle/industrial sensor data and stream it via MQTT to a cloud dashboard using HiveMQ and Node-red.
Currently working with randomized data stored in a local database.
## Setup
1. Install Python dependencies: `pip install paho-mqtt`
2. Install Node.js dependencies: `npm install`
3. Start Node-RED: `node-red`
4. Run sensor simulator: `python sensor_simulator.py`

Access dashboard at: `http://localhost:1880/ui`
