'''
Bridge from USB host to UART module.

Pitfall:
stdout redirection is impossible in micropython at the moment.
By default, stdout-writing functions will write to VCP and interfere with connection.
Therefore, do not use stdout-writing functions (print, ...) here or turn them off while using VCP.

Created on 08.10.2020

@author: LK
'''

from PyTrinamicMicro import PyTrinamicMicro
from PyTrinamicMicro.connections.tmcl_host_interface import tmcl_host_interface
from PyTrinamicMicro.platforms.motionpy.connections.uart_tmcl_interface import uart_tmcl_interface
from PyTrinamicMicro.platforms.motionpy.connections.usb_vcp_tmcl_interface import usb_vcp_tmcl_interface
from PyTrinamicMicro.TMCL_Bridge import TMCL_Bridge
import logging

# Prepare Logger
PyTrinamicMicro.set_logging_console_enabled(False)
logger = logging.getLogger(__name__)
logger.info("TMCL Bridge from USB to UART")

logger.info("Initializing interfaces ...")
host = usb_vcp_tmcl_interface()
module = uart_tmcl_interface()
bridge = TMCL_Bridge(host, [{"module":module}])
logger.info("Interfaces initialized.")

while(not(bridge.process())):
    pass

logger.info("Closing interfaces ...")
host.close()
module.close()
logger.info("Interfaces closed.")

logger.info("Bridge stopped.")
