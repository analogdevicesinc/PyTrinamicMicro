'''
Created on 20.10.2020

@author: LK
'''

from PyTrinamic.connections.ConnectionManager import ConnectionManager
from PyTrinamicMicro.connections.can_tmcl_interface import can_tmcl_interface
from PyTrinamicMicro.connections.rs232_tmcl_interface import rs232_tmcl_interface
from PyTrinamicMicro.connections.rs485_tmcl_interface import rs485_tmcl_interface
from PyTrinamicMicro.connections.uart_tmcl_interface import uart_tmcl_interface
from PyTrinamicMicro.connections.usb_vcp_tmcl_interface import usb_vcp_tmcl_interface

class ConnectionManagerMicro(ConnectionManager):

    @staticmethod
    def from_args(args=None):
        return ConnectionManager.from_args(ConnectionManagerMicro, args)

    @staticmethod
    def get_available_interfaces(self):
        return {
            "can_tmcl": can_tmcl_interface,
            "rs232_tmcl": rs232_tmcl_interface,
            "rs485_tmcl": rs485_tmcl_interface,
            "uart_tmcl": uart_tmcl_interface,
            "usb_vcp_tmcl": usb_vcp_tmcl_interface
        }
