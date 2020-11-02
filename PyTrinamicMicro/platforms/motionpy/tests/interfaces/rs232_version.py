'''
Test TMCL GET_FIRMWARE_VERSION via RS232 interface and module ID 1.

Created on 02.11.2020

@author: LK
'''

from PyTrinamicMicro.platforms.motionpy.connections.rs232_tmcl_interface import rs232_tmcl_interface
import logging
import re

VERSION_PATTERN = "^\d\d\d\dV\d\d\d$"

logger = logging.getLogger(__name__)
logger.info("Test interface RS232")

logger.info("Initializing interface.")
interface = rs232_tmcl_interface()

logger.info("Issuing GET_FIRMWARE_VERSION.")
value = interface.getVersionString()
logger.info("Value: {}.".format(value))

assert re.match(VERSION_PATTERN, value), "Invalid version string"
logger.info("Version string valid")
