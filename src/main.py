from utils import connect_can, send_can_message, receive_can_message, decrypt_can_message, encode_can_message, can_pipe
import can
import time
import json
import os

if __name__ == "__main__":
    # virtual CAN bus
    can_bus = connect_can(
        bus_type='virtual',
        channel='PCAN_VIRTUAL0',
        bitrate=500000
    )

    # physical CAN bus
    # can_bus = connect_can(    
    #     bus_type='pcan',
    #     channel='PCAN_USBBUS1',
    #     bitrate=500000
    # )

    if can_bus:
        # Example; manually created data
        SPEED = [0, 10, 20, 30, 40, 50, 60, 70]
        RPM = [0, 800, 1600, 2400, 3200, 4000, 4800, 5000]
        TEMP = [20, 22, 24, 26, 28, 30, 32, 34]
        TENSION = [12000, 12500, 13000, 13500, 14000, 14500, 15000, 15500]
        POWER = [100, 200, 300, 400, 500, 600, 700, 800]

        for i in range(8):
            rpm_low, rpm_high, tension_low, tension_high, power_low, power_high = encode_can_message(RPM[i], TENSION[i], POWER[i])
            message_data = [SPEED[i], rpm_low, rpm_high, TEMP[i], tension_low, tension_high, power_low, power_high]

            send_can_message(can_bus, 0x123, message_data)
            time.sleep(0.2)
            msg = receive_can_message(can_bus)

            if msg:
                speed, rpm, temp, tension, power = decrypt_can_message(msg.data)
                # comm via pipe
                can_pipe(msg, speed, rpm, temp, tension, power)
                
        can_bus.shutdown()  # Clean up the bus connection
    else:
        print("Failed to connect to the CAN bus.")