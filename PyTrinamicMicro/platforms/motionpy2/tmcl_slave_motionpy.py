from PyTrinamicMicro.TMCL_Slave import TMCL_Slave, TMCL_Slave_Status
# Imports
from PyTrinamic.TMCL import TMCL_Request, TMCL_Reply, TMCL_Status, TMCL
from PyTrinamic.modules.TMCM0960.TMCM0960 import TMCM0960
from PyTrinamicMicro import PyTrinamicMicro
import struct
import logging

class tmcl_slave_motionpy_status(TMCL_Slave_Status):

    def __init__(self):
        super().__init__()
        self.lin = [False]
        self.homing = [False]
        self.position_step = [False]
        self.position_absolute = [False]
        self.position_relative = [False]

class tmcl_slave_motionpy(TMCL_Slave, TMCM0960):

    def __init__(self, module_address=1, host_address=2, version_string="0960V100", build_version=0):
        super().__init__(module_address, host_address, version_string, build_version)
        self.status = tmcl_slave_motionpy_status()
        self.ap = [{
            self.APs.linear_homing_margin: int(0.2 * 0xFFFFFFFF),
            self.APs.linear_homing_hyst: int(0.5 * 0xFFFFFFFF),
            self.APs.linear_homing_status: self.ENUMs.HOMING_STATUS_IDLE,
            self.APs.linear_bound_low_step: 0,
            self.APs.linear_bound_low_actual: 0,
            self.APs.linear_bound_high_step: 0,
            self.APs.linear_bound_high_actual: 0,
            self.APs.linear_position_step: 0,
            self.APs.linear_position_absolute: 0,
            self.APs.linear_position_relative: 0,
            self.APs.linear_position_step_actual: 0,
            self.APs.linear_position_absolute_actual: 0,
            self.APs.linear_position_relative_actual: 0,
            self.APs.linear_velocity_actual: 0,
            self.APs.linear_velocity_position: 500000,
            self.APs.linear_velocity_homing: 500000,
            self.APs.linear_acceleration_position: 100000,
            self.APs.linear_acceleration_homing: 1000000,
            self.APs.linear_length: int(1000 * 0xFFFF)
        }]
        self.__logger = logging.getLogger(self.__module__)

    def _get_command_dict(self):
        out = super()._get_command_dict()
        out.update({
            TMCL.COMMANDS["TMCL_UF2"]: self.linear_distance
        })
        return out

    def linear_distance(self, request, reply):
        self.__logger.debug("linear_distance")
        func = {
            TMCM0960.ENUMs.LINEAR_DISTANCE_INIT: self.linear_distance_init,
            TMCM0960.ENUMs.LINEAR_DISTANCE_HOMING_START: self.linear_distance_homing_start,
            TMCM0960.ENUMs.LINEAR_DISTANCE_POSITION_STEP: self.linear_distance_position_step,
            TMCM0960.ENUMs.LINEAR_DISTANCE_POSITION_ABSOLUTE: self.linear_distance_position_absolute,
            TMCM0960.ENUMs.LINEAR_DISTANCE_POSITION_RELATIVE: self.linear_distance_position_relative
        }.get(request.commandType)
        if(func):
            reply = func(request, reply)
        else:
            reply.status = TMCL_Status.WRONG_TYPE
        return reply

    def linear_distance_init(self, request, reply):
        self.__logger.debug("linear_distance_init")
        self.status.lin[request.motorBank] = True
        return reply

    def linear_distance_homing_start(self, request, reply):
        self.__logger.debug("linear_distance_homing")
        self.status.homing[request.motorBank] = True
        self.ap[request.motorBank][self.APs.linear_homing_status] = self.ENUMs.HOMING_STATUS_INIT
        return reply

    def linear_distance_position_step(self, request, reply):
        self.__logger.debug("linear_distance_position_step")
        if(request.motorBank < len(self.ap)):
            #self.ap[request.motorBank][self.APs.linear_position_step] = request.value
            self.status.position_step[request.motorBank] = True
        else:
            reply.status = TMCL_Status.WRONG_TYPE
        return reply

    def linear_distance_position_absolute(self, request, reply):
        self.__logger.debug("linear_distance_position_absolute")
        if(request.motorBank < len(self.ap)):
            #self.ap[request.motorBank][self.APs.linear_position_absolute] = request.value
            self.status.position_absolute[request.motorBank] = True
        else:
            reply.status = TMCL_Status.WRONG_TYPE
        return reply

    def linear_distance_position_relative(self, request, reply):
        self.__logger.debug("linear_distance_position_relative")
        if(request.motorBank < len(self.ap)):
            #self.ap[request.motorBank][self.APs.linear_position_relative] = request.value
            self.status.position_relative[request.motorBank] = True
        else:
            reply.status = TMCL_Status.WRONG_TYPE
        return reply
