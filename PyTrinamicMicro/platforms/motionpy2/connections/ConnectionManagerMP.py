################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
Created on 20.10.2020

@author: LK
'''

from PyTrinamic.connections.ConnectionManager import ConnectionManager
from PyTrinamicMicro.platforms.motionpy2.connections.can_tmcl_interface import can_tmcl_interface
from PyTrinamicMicro.platforms.motionpy2.connections.rs232_tmcl_interface import rs232_tmcl_interface
from PyTrinamicMicro.platforms.motionpy2.connections.rs485_tmcl_interface import rs485_tmcl_interface
from PyTrinamicMicro.platforms.motionpy2.connections.uart_tmcl_interface import uart_tmcl_interface
from PyTrinamicMicro.platforms.motionpy2.connections.usb_vcp_tmcl_interface import usb_vcp_tmcl_interface

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
