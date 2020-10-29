'''
Created on 20.10.2020

@author: LK
'''

from PyTrinamic.connections.ConnectionManager import ConnectionManager
from PyTrinamicMicro.platforms.motionpy.connections.can_tmcl_interface import can_tmcl_interface
from PyTrinamicMicro.platforms.motionpy.connections.rs232_tmcl_interface import rs232_tmcl_interface
from PyTrinamicMicro.platforms.motionpy.connections.rs485_tmcl_interface import rs485_tmcl_interface
from PyTrinamicMicro.platforms.motionpy.connections.uart_tmcl_interface import uart_tmcl_interface
from PyTrinamicMicro.platforms.motionpy.connections.usb_vcp_tmcl_interface import usb_vcp_tmcl_interface

class ConnectionManagerMP(ConnectionManager):

    @staticmethod
    def from_args(args=None):
        return ConnectionManager.from_args(ConnectionManagerMP, args)

    @staticmethod
    def get_available_interfaces():
        return {
            "can_tmcl": can_tmcl_interface,
            "rs232_tmcl": rs232_tmcl_interface,
            "rs485_tmcl": rs485_tmcl_interface,
            "uart_tmcl": uart_tmcl_interface,
            "usb_vcp_tmcl": usb_vcp_tmcl_interface
        }
