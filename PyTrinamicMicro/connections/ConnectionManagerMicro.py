'''
Created on 20.10.2020

@author: LK
'''

from PyTrinamic.connections.ConnectionManager import ConnectionManager

class ConnectionManagerMicro(ConnectionManager):

    _DEFAULT_INTERFACE = "can_tmcl"
    _DEFAULT_PORT = "any"
    _DEFAULT_NO_PORT = []
    _DEFAULT_DATA_RATE = 115200
    _DEFAULT_HOST_ID = 2
    _DEFAULT_MODULE_ID = 1

    def _get_available_interfaces(self):
        from PyTrinamicMicro.connections.can_tmcl_interface import can_tmcl_interface
        from PyTrinamicMicro.connections.rs232_tmcl_interface import rs232_tmcl_interface
        from PyTrinamicMicro.connections.rs485_tmcl_interface import rs485_tmcl_interface
        from PyTrinamicMicro.connections.uart_tmcl_interface import uart_tmcl_interface
        from PyTrinamicMicro.connections.usb_vcp_tmcl_interface import usb_vcp_tmcl_interface
        return [
            ("can_tmcl", can_tmcl_interface, 0),
            ("rs232_tmcl", rs232_tmcl_interface, 9600),
            ("rs485_tmcl", rs485_tmcl_interface, 9600),
            ("uart_tmcl", uart_tmcl_interface, 9600),
            ("usb_vcp_tmcl", usb_vcp_tmcl_interface, 0)
        ]
