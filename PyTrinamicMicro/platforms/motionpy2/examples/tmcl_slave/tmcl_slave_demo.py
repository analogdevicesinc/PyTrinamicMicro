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
from PyTrinamicMicro.platforms.motionpy2.connections.usb_vcp_tmcl_interface import usb_vcp_tmcl_interface
from PyTrinamicMicro.platforms.motionpy2.tmcl_slave_demo import tmcl_slave_demo
from PyTrinamic.modules.TMCM1270.TMCM_1270 import TMCM_1270
from PyTrinamicMicro.platforms.motionpy2.connections.can_tmcl_interface import can_tmcl_interface
from PyTrinamicMicro import PyTrinamicMicro
import struct
import logging
import time

# Prepare Logger
PyTrinamicMicro.set_logging_console_enabled(False)
logger = logging.getLogger(__name__)
logger.info("TMCL Slave on USB_VCP interface")

# Main program
lin = None
logger.info("Initializing interface ...")
con = usb_vcp_tmcl_interface()
slave = tmcl_slave_demo()
module = TMCM_1270(can_tmcl_interface())
module.setMaxAcceleration(0, 100000)
logger.info("Interface initialized.")

t = 0

while(not(slave.status.stop)):
    # Handle connection
    if(con.request_available()):
        logger.debug("Request available.")
        request = con.receive_request()
        if(not(slave.filter(request))):
            continue
        logger.debug("Request for this slave detected.")
        reply = slave.handle_request(request)
        con.send_reply(reply)
    # Handle flags
    if(slave.status.demo[0]):
        if(t == 0):
            t = time.time()
            module.rotate(0, 100000)
        if(time.time() - t > 3):
            module.stop(0)
            t = 0
            slave.status.demo[0] = False

logger.info("Closing interface ...")
con.close()
logger.info("Interface closed.")

logger.info("Slave stopped.")
