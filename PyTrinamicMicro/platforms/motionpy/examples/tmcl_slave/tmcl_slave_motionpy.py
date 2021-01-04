'''
Act as TMCL slave over USB.

Pitfall:
stdout redirection is impossible in micropython at the moment.
By default, stdout-writing functions will write to VCP and interfere with connection.
Therefore, do not use stdout-writing functions (print, ...) here or turn them off while using VCP.

Created on 06.10.2020

@author: LK
'''

# Imports
from PyTrinamicMicro.platforms.motionpy.connections.usb_vcp_tmcl_interface import usb_vcp_tmcl_interface
from PyTrinamicMicro.platforms.motionpy.tmcl_slave_motionpy import tmcl_slave_motionpy
from PyTrinamicMicro.platforms.motionpy.modules.linear_distance import linear_distance
from PyTrinamic.modules.TMCM1240.TMCM_1240 import TMCM_1240
from PyTrinamicMicro.platforms.motionpy.modules.hc_sr04_multi import hc_sr04_multi
from PyTrinamicMicro.platforms.motionpy.modules.MCP23S08 import MCP23S08
from PyTrinamicMicro.platforms.motionpy.connections.rs485_tmcl_interface import rs485_tmcl_interface
from PyTrinamicMicro import PyTrinamicMicro
import struct
import logging

# Prepare Logger
PyTrinamicMicro.set_logging_console_enabled(False)
logger = logging.getLogger(__name__)
logger.info("TMCL Slave on USB_VCP interface")

# Main program
lin = None
logger.info("Initializing interface ...")
con = usb_vcp_tmcl_interface()
slave = tmcl_slave_motionpy()
module = TMCM_1240(rs485_tmcl_interface(data_rate=115200))
module.setMaxAcceleration(0, 100000)
logger.info("Interface initialized.")

while(not(slave.status.stop)):
    # Handle connection
    if(con.request_available()):
        logger.debug("Request available.")
        request = con.receive_request()
        if(not(slave.filter(request))):
            continue
        logger.debug("Request for this slave detected.")
        reply = slave.handle_request(request)
        con.send_reply(reply)
    # Handle flags
    if(slave.status.lin[0]):
        lin = linear_distance(hc_sr04_multi(avg_window=100), 1, module)
        slave.status.lin[0] = False
    if(slave.status.homing[0]):
        slave.ap[0][slave.APs.linear_homing_status] = lin.homing(
            slave.ap[0][slave.APs.linear_homing_status],
            slave.ap[0][slave.APs.linear_length] / 0xFFFF,
            slave.ap[0][slave.APs.linear_velocity_homing],
            slave.ap[0][slave.APs.linear_acceleration_homing],
            slave.ap[0][slave.APs.linear_homing_margin] / 0xFFFFFFFF,
            slave.ap[0][slave.APs.linear_homing_hyst] / 0xFFFFFFFF
        )
    if(slave.status.position_step[0]):
        lin.position_step(slave.ap[0][slave.APs.linear_position_step], slave.ap[0][slave.APs.linear_velocity_position], slave.ap[0][slave.APs.linear_acceleration_position])
        slave.status.position_step[0] = False
    if(slave.status.position_relative[0]):
        lin.position_relative(slave.ap[0][slave.APs.linear_position_relative] / 0xFFFFFFFF, slave.ap[0][slave.APs.linear_velocity_position], slave.ap[0][slave.APs.linear_acceleration_position])
        slave.status.position_relative[0] = False
    if(slave.status.position_absolute[0]):
        lin.position_absolute(slave.ap[0][slave.APs.linear_position_absolute] / 0xFFFF, slave.ap[0][slave.APs.linear_velocity_position], slave.ap[0][slave.APs.linear_acceleration_position])
        slave.status.position_absolute[0] = False
    # Write back APs
    if(lin):
        slave.ap[0][slave.APs.linear_position_step_actual] = lin.position_step()
        slave.ap[0][slave.APs.linear_position_absolute_actual] = int(lin.position_absolute() * 0xFFFF)
        slave.ap[0][slave.APs.linear_velocity_actual] = lin.module.getActualVelocity(0)
        if(slave.ap[0][slave.APs.linear_homing_status] == slave.ENUMs.HOMING_STATUS_DONE):
            slave.ap[0][slave.APs.linear_position_relative_actual] = int(lin.position_relative() * 0xFFFFFFFF)
            slave.ap[0][slave.APs.linear_bound_low_step] = lin.bounds[0][1]
            slave.ap[0][slave.APs.linear_bound_low_actual] = int(lin.bounds[0][0] * 0xFFFF)
            slave.ap[0][slave.APs.linear_bound_high_step] = lin.bounds[1][1]
            slave.ap[0][slave.APs.linear_bound_high_actual] = int(lin.bounds[1][0] * 0xFFFF)

logger.info("Closing interface ...")
con.close()
logger.info("Interface closed.")

logger.info("Slave stopped.")
