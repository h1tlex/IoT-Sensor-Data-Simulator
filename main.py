from utils import connect_can, send_can_message, receive_can_message, decrypt_can_message
import can
import time

    
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

    # IDs :
    # 0x123 - Speed + RPM
    # 0x124 - Temperature + Humidity
    # 0x125 - Tension + Active power

    if can_bus:
        # Example; manually create a message for speed and RPM
        # Format: [speed, rpm_low_byte, rpm_high_byte]
        SPEED = [0, 10, 20, 30, 40, 50, 60, 70]
        RPM = [0, 800, 1600, 2400, 3200, 4000, 4800, 5000]

        for i in range(len(SPEED)):

            # Encode RPM as little-endian (low byte first)
            rpm_low = RPM[i] & 0xFF          # Get the lower 8 bits
            rpm_high = (RPM[i] >> 8) & 0xFF  # Get the upper 8 bits

            message_data = [SPEED[i], rpm_low, rpm_high]
            send_can_message(can_bus, 0x123, message_data)
            time.sleep(0.2)
            msg = receive_can_message(can_bus)

            if msg:
                speed, rpm = decrypt_can_message(msg.data)
                if speed is not None and rpm is not None:
                    print(f"Decrypted Speed: {speed} km/h, RPM: {rpm}")
                else:
                    print("Failed to decrypt message data.")   
                
        can_bus.shutdown()  # Clean up the bus connection