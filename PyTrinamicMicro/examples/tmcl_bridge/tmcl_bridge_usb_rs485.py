'''
Bridge from USB host to RS485 module.

Pitfall:
stdout redirection is impossible in micropython at the moment.
By default, stdout-writing functions will write to VCP and interfere with connection.
Therefore, do not use stdout-writing functions (print, ...) here or turn them off while using VCP.

Created on 08.10.2020

@author: LK
'''

from PyTrinamicMicro.connections.tmcl_host_interface import tmcl_host_interface
from PyTrinamicMicro.connections.rs485_tmcl_interface import rs485_tmcl_interface
from PyTrinamicMicro.connections.usb_vcp_tmcl_interface import usb_vcp_tmcl_interface
from PyTrinamicMicro.TMCL_Bridge import TMCL_Bridge
from PyTrinamic.TMCL import TMCL_Command
import logging

# Prepare Logger
logger = logging.getLogger(__name__)
logger.info("TMCL Bridge from USB to RS485")

logger.info("Initializing interfaces ...")
host = usb_vcp_tmcl_interface()
module = rs485_tmcl_interface()
bridge = TMCL_Bridge(host, module)
logger.info("Interfaces initialized.")

while(not(bridge.process())):
    #logger.debug("Processed request.")
    pass

logger.info("Closing interfaces ...")
host.close()
module.close()
logger.info("Interfaces closed.")

logger.info("Bridge stopped.")
