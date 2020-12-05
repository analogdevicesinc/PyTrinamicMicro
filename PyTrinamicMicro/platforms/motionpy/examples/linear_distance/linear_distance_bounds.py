from PyTrinamicMicro.platforms.motionpy.modules.linear_distance import linear_distance
from PyTrinamic.ic.TMC5130.TMC5130 import TMC5130
from PyTrinamicMicro.platforms.motionpy.modules.hc_sr04_multi import hc_sr04_multi
from PyTrinamicMicro.platforms.motionpy.modules.MCP23S08 import MCP23S08
from PyTrinamicMicro.platforms.motionpy.connections.uart_ic_interface import uart_ic_interface

mc = TMC5130(connection=uart_ic_interface(single_wire=True), comm=TMC5130.COMM_UART)

mc.writeRegister(0x10, 0x00071703)
mc.writeRegister(0x6C, 0x000101D5)
mc.writeRegister(0x70, 0x000500C8)

lin = linear_distance(
    sensor = hc_sr04_multi(avg_window=100),
    sensor_index = 1,
    mc = mc
)

lin.homing()

print(lin.bounds)
