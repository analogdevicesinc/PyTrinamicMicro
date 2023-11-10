################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
Test TMCL GET_FIRMWARE_VERSION via CAN interface and module ID 1.

Created on 02.11.2020

@author: LK
'''

from PyTrinamicMicro.platforms.motionpy2.connections.can_tmcl_interface import can_tmcl_interface
import logging
import re

VERSION_PATTERN = "^\d\d\d\dV\d\d\d$"

logger = logging.getLogger(__name__)
logger.info("Test interface CAN")

logger.info("Initializing interface.")
interface = can_tmcl_interface()

logger.info("Issuing GET_FIRMWARE_VERSION.")
value = interface.getVersionString()
logger.info("Value: {}.".format(value))

assert re.match(VERSION_PATTERN, value), "Invalid version string"
logger.info("Version string valid")
