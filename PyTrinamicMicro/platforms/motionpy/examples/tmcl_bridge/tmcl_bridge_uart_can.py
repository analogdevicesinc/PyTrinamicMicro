'''
Bridge from UART host to CAN module.

Created on 07.10.2020

@author: LK
'''

from PyTrinamicMicro.connections.tmcl_host_interface import tmcl_host_interface
from PyTrinamicMicro.platforms.motionpy.connections.can_tmcl_interface import can_tmcl_interface
from PyTrinamicMicro.platforms.motionpy.connections.uart_tmcl_interface import uart_tmcl_interface
from PyTrinamicMicro.TMCL_Bridge import TMCL_Bridge
from PyTrinamic.TMCL import TMCL
import logging

# Prepare Logger
logger = logging.getLogger(__name__)
logger.info("TMCL Bridge from UART to CAN")

# When using a CAN module, Checksum needs to be recalculated.

request_command = 0

def request_callback(request):
    global request_command
    request_command = request.command
    return request

def reply_callback(reply):
    if(request_command != TMCL.COMMANDS["GET_FIRMWARE_VERSION"]):
        reply.calculate_checksum()
    return reply

logger.info("Initializing interfaces ...")
host = uart_tmcl_interface()
module = can_tmcl_interface()
bridge = TMCL_Bridge(host, [{"module":module, "request_callback":request_callback, "reply_callback":reply_callback}])
logger.info("Interfaces initialized.")

while(not(bridge.process())):
    pass

logger.info("Closing interfaces ...")
host.close()
module.close()
logger.info("Interfaces closed.")

logger.info("Bridge stopped.")
