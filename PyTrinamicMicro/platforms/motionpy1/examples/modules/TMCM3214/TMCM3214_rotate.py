################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
Rotate the motor with TMCM3214 using RS485 interface.

Created on 19.04.2021

@author: LK
'''

from PyTrinamic.modules.TMCM3214.TMCM_3214 import TMCM_3214
from PyTrinamicMicro.platforms.motionpy1.connections.rs485_tmcl_interface import rs485_tmcl_interface
from pyb import Pin
import time

con = rs485_tmcl_interface(data_rate=9600)
module = TMCM_3214(con)

module.rotate(0, 10000)
time.sleep(5)
module.stop(0)

con.close()
