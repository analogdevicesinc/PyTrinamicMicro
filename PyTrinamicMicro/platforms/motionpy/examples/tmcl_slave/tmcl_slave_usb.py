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
from PyTrinamicMicro.platforms.motionpy.connections.usb_vcp_tmcl_interface import usb_vcp_tmcl_interface
from PyTrinamicMicro.TMCL_Slave import TMCL_Slave_Bridge
from PyTrinamicMicro import PyTrinamicMicro
import struct
import logging

# Constants
MODULE_ADDRESS = 1
HOST_ADDRESS = 2
MODULE_ID_STRING = "0021"
VERSION_STRING = MODULE_ID_STRING + "V100"
BUILD_VERSION = 0

# Prepare Logger
PyTrinamicMicro.set_logging_console_enabled(False)
logger = logging.getLogger(__name__)
logger.info("TMCL Slave on USB_VCP interface")

# Main program

logger.info("Initializing interface ...")
con = usb_vcp_tmcl_interface()
slave = TMCL_Slave_Bridge(MODULE_ADDRESS, HOST_ADDRESS, VERSION_STRING, BUILD_VERSION)
logger.info("Interface initialized.")

while(not(slave.status.stop)):
    if(con.request_available()):
        logger.debug("Request available.")
        request = con.receive_request()
        if(not(slave.filter(request))):
            continue
        logger.debug("Request for this slave detected.")
        reply = slave.handle_request(request)
        con.send_reply(reply)

logger.info("Closing interface ...")
con.close()
logger.info("Interface closed.")

logger.info("Slave stopped.")
