'''
Act as TMCL slave over USB.

Pitfall:
stdout redirection is impossible in micropython at the moment.
By default, stdout-writing functions will write to VCP and interfere with connection.
Therefore, do not use stdout-writing functions (print, ...) here or turn them off while using VCP.

Created on 06.10.2020

@author: LK
'''

# Imports
from PyTrinamicMicro.connections.usb_vcp_tmcl_interface import usb_vcp_tmcl_interface
from PyTrinamicMicro.TMCL_Slave import TMCL_Slave_Main
import struct

# Constants
MODULE_ADDRESS = 1
HOST_ADDRESS = 2
MODULE_ID_STRING = "0021"
VERSION_STRING = MODULE_ID_STRING + "V100"
BUILD_VERSION = 0

# Main program

con = usb_vcp_tmcl_interface()
slave = TMCL_Slave_Main(MODULE_ADDRESS, HOST_ADDRESS, VERSION_STRING, BUILD_VERSION)

while(not(slave.get_status().stop)):
    if(con.request_available()):
        request = con.receive_request()
        if(not(slave.filter(request))):
            continue
        reply = slave.handle_request(request)
        con.send_reply(reply)

con.close()
