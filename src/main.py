from utils import init_can, create_ipc_sender, start_physical_can, start_virtual_can
import os

if __name__ == "__main__":

    # "v" for virtual CAN bus, "p" for physical USB/CAN bus
    if len(os.sys.argv) != 2 or os.sys.argv[1] not in ['v', 'p']:
        print("Usage: python main.py <can_bus_type> ('v' for virtual, 'p' for physical)")
        exit(1)

    can_bus_type = os.sys.argv[1]
    can_bus = init_can(can_bus_type)

    # connect to ipc
    client_socket = create_ipc_sender()

    if can_bus:
        if can_bus_type == 'v':
            start_virtual_can(can_bus, client_socket)
        else:
            start_physical_can(can_bus, client_socket)
    else:
        print("Failed to initialize CAN bus. Exiting.")
        exit(2)

    exit(0)