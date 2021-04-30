from PyTrinamicMicro.TMCL_Slave import TMCL_Slave, TMCL_Slave_Status
# Imports
from PyTrinamic.TMCL import TMCL_Request, TMCL_Reply, TMCL_Status, TMCL
from PyTrinamic.modules.TMCM0960.TMCM0960 import TMCM0960
from PyTrinamicMicro import PyTrinamicMicro
import struct
import logging

class tmcl_slave_demo_status(TMCL_Slave_Status):

    def __init__(self):
        super().__init__()
        self.demo = [False]

class tmcl_slave_demo(TMCL_Slave, TMCM0960):

    def __init__(self, module_address=1, host_address=2, version_string="0960V100", build_version=0):
        super().__init__(module_address, host_address, version_string, build_version)
        self.status = tmcl_slave_demo_status()
        self.ap = list(dict())
        self.__logger = logging.getLogger(self.__module__)

    def _get_command_dict(self):
        out = super()._get_command_dict()
        out.update({
            TMCL.COMMANDS["TMCL_UF2"]: self.demo
        })
        return out

    def demo(self, request, reply):
        self.__logger.debug("demo")
        self.status.demo[request.motorBank] = True
        return reply
