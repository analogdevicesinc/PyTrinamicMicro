################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
Rotate the motor with TMCM1270 using CAN interface.

Created on 05.10.2020

@author: LK
'''

from PyTrinamic.modules.TMCM1270.TMCM_1270 import TMCM_1270
from PyTrinamicMicro.platforms.motionpy1.connections.can_tmcl_interface import can_tmcl_interface
from pyb import Pin
import time

con = can_tmcl_interface()
module = TMCM_1270(con)
en = Pin(Pin.cpu.A4, Pin.OUT_PP)

en.low()

module.rotate(0, 1000)
time.sleep(5)
module.stop(0)

en.high()

con.close()
