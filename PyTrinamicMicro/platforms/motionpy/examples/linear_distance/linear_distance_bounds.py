from PyTrinamicMicro.platforms.motionpy.modules.linear_distance import linear_distance
from PyTrinamic.modules.TMCM1240.TMCM_1240 import TMCM_1240
from PyTrinamicMicro.platforms.motionpy.modules.hc_sr04_multi import hc_sr04_multi
from PyTrinamicMicro.platforms.motionpy.modules.MCP23S08 import MCP23S08
from PyTrinamicMicro.platforms.motionpy.connections.rs485_tmcl_interface import rs485_tmcl_interface

module = TMCM_1240(rs485_tmcl_interface())
module.setMaxAcceleration(0, 100000)

lin = linear_distance(
    sensor = hc_sr04_multi(avg_window=100),
    sensor_index = 1,
    module = module
)

lin.homing_direct(velocity=100000)

print(lin.bounds)
