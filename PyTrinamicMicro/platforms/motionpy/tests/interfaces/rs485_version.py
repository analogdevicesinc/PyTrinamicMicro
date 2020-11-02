'''
Test TMCL GET_FIRMWARE_VERSION via RS485 interface and module ID 1.

Created on 02.11.2020

@author: LK
'''

from PyTrinamicMicro.platforms.motionpy.connections.rs485_tmcl_interface import rs485_tmcl_interface
import logging
import re

VERSION_PATTERN = "^\d\d\d\dV\d\d\d$"

logger = logging.getLogger(__name__)
logger.info("Test interface RS485")

logger.info("Initializing interface.")
interface = rs485_tmcl_interface()

logger.info("Issuing GET_FIRMWARE_VERSION.")
value = interface.getVersionString()
logger.info("Value: {}.".format(value))

assert re.match(VERSION_PATTERN, value), "Invalid version string"
logger.info("Version string valid")
