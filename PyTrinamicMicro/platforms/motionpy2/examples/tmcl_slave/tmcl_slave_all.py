'''
Act as TMCL slave over all interfaces.

Created on 06.10.2020

@author: LK
'''

# Imports
from PyTrinamicMicro.platforms.motionpy2.connections.usb_vcp_tmcl_interface import usb_vcp_tmcl_interface
from PyTrinamicMicro.platforms.motionpy2.connections.rs232_tmcl_interface import rs232_tmcl_interface
from PyTrinamicMicro.platforms.motionpy2.connections.rs485_tmcl_interface import rs485_tmcl_interface
from PyTrinamicMicro.platforms.motionpy2.connections.can_tmcl_interface import can_tmcl_interface
from PyTrinamicMicro.TMCL_Slave import TMCL_Slave_Bridge
from PyTrinamicMicro import PyTrinamicMicro
import struct
import logging

# Constants
MODULE_ADDRESS = 1
HOST_ADDRESS = 2
MODULE_ID_STRING = "0960"
VERSION_STRING = MODULE_ID_STRING + "V100"
BUILD_VERSION = 0

# Prepare Logger
PyTrinamicMicro.set_logging_console_enabled(False)
logger = logging.getLogger(__name__)
logger.info("TMCL Slave on all interfaces")

# Main program

logger.info("Initializing interfaces ...")
cons = [
    #usb_vcp_tmcl_interface(),
    can_tmcl_interface()
    rs232_tmcl_interface(),
    rs485_tmcl_interface(),
]
slave = TMCL_Slave_Bridge(MODULE_ADDRESS, HOST_ADDRESS, VERSION_STRING, BUILD_VERSION)
logger.info("Interfaces initialized.")

while(not(slave.status.stop)):
    for con in cons:
        if(con.request_available()):
            logger.debug("Request available.")
            request = con.receive_request()
            if(not(slave.filter(request))):
                continue
            logger.debug("Request for this slave detected.")
            reply = slave.handle_request(request)
            con.send_reply(reply)

logger.info("Closing interfaces ...")
for con in cons:
    con.close()
logger.info("Interfaces closed.")

logger.info("Slave stopped.")
