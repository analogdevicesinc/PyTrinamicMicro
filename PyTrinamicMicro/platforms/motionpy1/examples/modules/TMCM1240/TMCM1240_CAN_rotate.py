################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
Rotate the motor with TMCM1240 using CAN interface.

Created on 21.10.2020

@author: LK
'''

from PyTrinamic.modules.TMCM1240.TMCM_1240 import TMCM_1240
from PyTrinamicMicro.platforms.motionpy1.connections.can_tmcl_interface import can_tmcl_interface
import time

con = can_tmcl_interface()
module = TMCM_1240(con)

module.rotate(50000)
time.sleep(5)
module.stop()

con.close()
