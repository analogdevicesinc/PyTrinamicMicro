'''
Test TMCL GET_FIRMWARE_VERSION via several interfaces and module ID 1.

Created on 02.11.2020

@author: LK
'''

from PyTrinamicMicro.platforms.motionpy.connections.can_tmcl_interface import can_tmcl_interface
from PyTrinamicMicro.platforms.motionpy.connections.rs232_tmcl_interface import rs232_tmcl_interface
from PyTrinamicMicro.platforms.motionpy.connections.rs485_tmcl_interface import rs485_tmcl_interface
import logging
import re

VERSION_PATTERN = "^\d\d\d\dV\d\d\d$"

logger = logging.getLogger(__name__)
logger.info("Test GET_FIRMWARE_VERSION for CAN, RS232 and RS485 interfaces.")

logger.info("Initializing interfaces.")
interfaces = set()
interfaces.add(can_tmcl_interface())
interfaces.add(rs232_tmcl_interface())
interfaces.add(rs485_tmcl_interface())

for interface in interfaces:
    logger.info("Issuing GET_FIRMWARE_VERSION on interface {}.".format(interface))
    value = interface.getVersionString()
    logger.info("Value: {}.".format(value))
    assert re.match(VERSION_PATTERN, value), "Invalid version string"
    logger.info("Version string valid")
