################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

from PyTrinamicMicro.TMCL_Slave import TMCL_Slave, TMCL_Slave_Status
# Imports
from PyTrinamic.TMCL import TMCL_Request, TMCL_Reply, TMCL_Status, TMCL_Command
from PyTrinamic.modules.TMCM0960.TMCM0960 import TMCM0960
from PyTrinamicMicro import PyTrinamicMicro
import struct
import logging

class tmcl_slave_dummy(TMCL_Slave):

    def __init__(self, module_address=1, host_address=2, version_string="0012V308", build_version=0):
        super().__init__(module_address, host_address, version_string, build_version)
        self.status = TMCL_Slave_Status()
        self.__logger = logging.getLogger(self.__module__)

    def _get_command_func(self, command):
        return self.command

    def command(self, request, reply):
        self.__logger.debug("command {{{},{}}}".format(request, reply))
