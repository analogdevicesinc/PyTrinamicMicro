################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

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
from PyTrinamicMicro.platforms.motionpy2.tmcl_slave_dummy import tmcl_slave_dummy
from PyTrinamicMicro import PyTrinamicMicro
import struct
import logging

# Prepare Logger
PyTrinamicMicro.set_logging_console_enabled(False)
logger = logging.getLogger(__name__)
logger.info("TMCL Slave on USB_VCP interface")

# Main program
lin = None
logger.info("Initializing interface ...")
con = usb_vcp_tmcl_interface()
slave = tmcl_slave_dummy()
logger.info("Interface initialized.")

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

logger.info("Closing interface ...")
con.close()
logger.info("Interface closed.")

logger.info("Slave stopped.")
