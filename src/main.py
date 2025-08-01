from utils import connect_can, create_ipc_sender, start_can_communication

if __name__ == "__main__":


    # virtual CAN bus
    # can_bus = connect_can(
    #    bus_type='virtual',
    #    channel='PCAN_VIRTUAL0',
    #    bitrate=500000 
    #)

    # physical CAN bus
    can_bus = connect_can(    
        bus_type='pcan',
        channel='PCAN_USBBUS1',
        bitrate=500000
    )

    # connect to ipc
    client_socket = create_ipc_sender()

    if can_bus:
        traffic = {
            'speed' : None,
            'rpm' : None,
            'temp' : None,
            'tension' : None,
            'power' : 0
        }

        start_can_communication(can_bus, traffic, client_socket)
                
        can_bus.shutdown()  # Clean up the bus connection