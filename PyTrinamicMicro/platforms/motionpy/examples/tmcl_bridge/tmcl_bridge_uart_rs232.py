'''
Bridge from UART host to RS232 module.

Created on 07.10.2020

@author: LK
'''

from PyTrinamicMicro.connections.tmcl_host_interface import tmcl_host_interface
from PyTrinamicMicro.platforms.motionpy.connections.rs232_tmcl_interface import rs232_tmcl_interface
from PyTrinamicMicro.platforms.motionpy.connections.uart_tmcl_interface import uart_tmcl_interface
from PyTrinamicMicro.TMCL_Bridge import TMCL_Bridge
import logging

# Prepare Logger
logger = logging.getLogger(__name__)
logger.info("TMCL Bridge from UART to RS232")

logger.info("Initializing interfaces ...")
host = uart_tmcl_interface()
module = rs232_tmcl_interface()
bridge = TMCL_Bridge(host, [{"module":module}])
logger.info("Interfaces initialized.")

while(not(bridge.process())):
    pass

logger.info("Closing interfaces ...")
host.close()
module.close()
logger.info("Interfaces closed.")

logger.info("Bridge stopped.")
