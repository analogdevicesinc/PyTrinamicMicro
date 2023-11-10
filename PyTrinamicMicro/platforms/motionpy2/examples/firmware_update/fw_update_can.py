################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
Update firmware of attached board via CAN.

Created on 19.10.2020

@author: LK
'''

from PyTrinamicMicro.platforms.motionpy2.connections.can_tmcl_interface import can_tmcl_interface
from PyTrinamicMicro.tmcl_bootloader import *
import logging
import time

FIRMWARE = "firmware.hex"
MODULE_ID = 1

con = can_tmcl_interface()
con.sendBoot()
time.sleep(3.0)
boot = tmcl_bootloader(con, MODULE_ID)
boot.update_firmware(open(FIRMWARE, "rt"), start=True, checksum_error=False, verify_hex=True, verify_bootloader=True)
