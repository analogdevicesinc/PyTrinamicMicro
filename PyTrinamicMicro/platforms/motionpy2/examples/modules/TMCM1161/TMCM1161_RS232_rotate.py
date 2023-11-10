################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
Rotate the motor with TMCM1161 using RS232 interface.

Created on 06.10.2020

@author: LK
'''

from PyTrinamic.modules.TMCM1161.TMCM_1161 import TMCM_1161
from PyTrinamicMicro.platforms.motionpy2.connections.rs232_tmcl_interface import rs232_tmcl_interface
import time

con = rs232_tmcl_interface()
module = TMCM_1161(con)

module.rotate(0, 1000)
time.sleep(5)
module.stop(0)

con.close()
