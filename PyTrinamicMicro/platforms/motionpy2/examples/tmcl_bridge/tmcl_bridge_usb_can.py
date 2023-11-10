################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
Bridge from USB host to CAN module.

Pitfall:
stdout redirection is impossible in micropython at the moment.
By default, stdout-writing functions will write to VCP and interfere with connection.
Therefore, do not use stdout-writing functions (print, ...) here or turn them off while using VCP.

Created on 07.10.2020

@author: LK
'''

from PyTrinamicMicro import PyTrinamicMicro
from PyTrinamicMicro.connections.tmcl_host_interface import tmcl_host_interface
from PyTrinamicMicro.platforms.motionpy2.connections.can_tmcl_interface import can_tmcl_interface
from PyTrinamicMicro.platforms.motionpy2.connections.usb_vcp_tmcl_interface import usb_vcp_tmcl_interface
from PyTrinamicMicro.TMCL_Bridge import TMCL_Bridge
from PyTrinamic.TMCL import TMCL
import logging

# Prepare Logger
PyTrinamicMicro.set_logging_console_enabled(False)
logger = logging.getLogger(__name__)
logger.info("TMCL Bridge from USB to CAN")

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
host = usb_vcp_tmcl_interface()
modules = [{
    "module": can_tmcl_interface(),
    "request_callback": request_callback,
    "reply_callback": reply_callback
}]
bridge = TMCL_Bridge(host, modules)
logger.info("Interfaces initialized.")

while(not(bridge.process())):
    pass

logger.info("Closing interfaces ...")
host.close()
module.close()
logger.info("Interfaces closed.")

logger.info("Bridge stopped.")
