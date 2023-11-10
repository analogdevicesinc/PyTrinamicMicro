################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

from PyTrinamicMicro.platforms.motionpy2.modules.linear_distance import linear_distance
from PyTrinamic.modules.TMCM1240.TMCM_1240 import TMCM_1240
from PyTrinamicMicro.platforms.motionpy2.modules.hc_sr04_multi import hc_sr04_multi
from PyTrinamicMicro.platforms.motionpy2.modules.MCP23S08 import MCP23S08
from PyTrinamicMicro.platforms.motionpy2.connections.rs485_tmcl_interface import rs485_tmcl_interface

module = TMCM_1240(rs485_tmcl_interface())
module.setMaxAcceleration(0, 100000)

lin = linear_distance(
    sensor = hc_sr04_multi(avg_window=100),
    sensor_index = 1,
    module = module
)

lin.homing_direct(velocity=100000)

print(lin.bounds)
