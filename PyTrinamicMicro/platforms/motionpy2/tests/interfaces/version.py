################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
Test TMCL GET_FIRMWARE_VERSION via several interfaces and module ID 1.

Created on 02.11.2020

@author: LK
'''

from PyTrinamicMicro.platforms.motionpy2.connections.can_tmcl_interface import can_tmcl_interface
from PyTrinamicMicro.platforms.motionpy2.connections.rs232_tmcl_interface import rs232_tmcl_interface
from PyTrinamicMicro.platforms.motionpy2.connections.rs485_tmcl_interface import rs485_tmcl_interface
import logging
import re

VERSION_PATTERN = "^\d\d\d\dV\d\d\d$"

logger = logging.getLogger(__name__)
logger.info("Test GET_FIRMWARE_VERSION for CAN, RS232 and RS485 interfaces.")

logger.info("Initializing interfaces.")
interfaces = [
    can_tmcl_interface(),
    rs232_tmcl_interface(),
    rs485_tmcl_interface()
]

for interface in interfaces:
    logger.info("Issuing GET_FIRMWARE_VERSION on interface {}.".format(interface))
    value = interface.getVersionString()
    logger.info("Value: {}.".format(value))
    assert re.match(VERSION_PATTERN, value), "Invalid version string"
    logger.info("Version string valid")
