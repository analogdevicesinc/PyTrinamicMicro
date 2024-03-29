################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
Bridge from UART host to RS485 module.

Created on 14.10.2020

@author: LK
'''

from PyTrinamicMicro.connections.tmcl_host_interface import tmcl_host_interface
from PyTrinamicMicro.platforms.motionpy1.connections.rs485_tmcl_interface import rs485_tmcl_interface
from PyTrinamicMicro.platforms.motionpy1.connections.uart_tmcl_interface import uart_tmcl_interface
from PyTrinamicMicro.TMCL_Bridge import TMCL_Bridge
import logging

# Prepare Logger
logger = logging.getLogger(__name__)
logger.info("TMCL Bridge from UART to RS485")

logger.info("Initializing interfaces ...")
host = uart_tmcl_interface()
module = rs485_tmcl_interface()
bridge = TMCL_Bridge(host, [{"module":module}])
logger.info("Interfaces initialized.")

while(not(bridge.process())):
    pass

logger.info("Closing interfaces ...")
host.close()
module.close()
logger.info("Interfaces closed.")

logger.info("Bridge stopped.")
