'''
Created on 07.10.2020

@author: LK
'''

# Imports
from PyTrinamic.TMCL import TMCL_Request, TMCL_Reply, TMCL_Status, TMCL
from PyTrinamic.modules.TMCM0960.TMCM0960 import TMCM0960
from PyTrinamicMicro import PyTrinamicMicro
import struct
import logging


class TMCL_Slave_Status(object):

    def __init__(self):
        self.stop = False


class TMCL_Slave(TMCM0960):

    def __init__(self, module_address=1, host_address=2, version_string="0960V100", build_version=0):
        self.__module_address = module_address
        self.__host_address = host_address
        self.__version_string = version_string
        self.__build_version = build_version
        self.status = TMCL_Slave_Status()
        self.__subscript = ""
        self.__logger = logging.getLogger(self.__module__)
        self.gp = dict()
        self.ap = list()

    def filter(self, request):
        return (request.moduleAddress == self.__module_address)

    def _get_command_func(self):
        return {
            TMCL.COMMANDS["GET_FIRMWARE_VERSION"]: self.get_version,
            TMCL.COMMANDS["SGP"]: self.set_global_parameter,
            TMCL.COMMANDS["GGP"]: self.get_global_parameter,
            TMCL.COMMANDS["SAP"]: self.set_axis_parameter,
            TMCL.COMMANDS["GAP"]: self.get_axis_parameter,
            TMCL.COMMANDS["TMCL_UF0"]: self.stop,
            TMCL.COMMANDS["TMCL_UF1"]: self.subscript
        }

    def handle_request(self, request):
        reply = TMCL_Reply(reply_address=self.__host_address, module_address=self.__module_address, status=TMCL_Status.SUCCESS, value=0, command=request.command)

        command_func = self._get_command_func().get(request.command)
        if(command_func):
            reply = command_func(request, reply)
        else:
            reply.status = TMCL_Status.INVALID_COMMAND

        if(not(reply.special)):
            #reply.reply_address = self.__host_address
            reply.calculate_checksum()

        return reply

    def get_version(self, request, reply):
        self.__logger.debug("get_version")
        func = {
            TMCM0960.ENUMs.VERSION_FORMAT_ASCII: self.get_version_ascii,
            TMCM0960.ENUMs.VERSION_FORMAT_BINARY: self.get_version_binary,
            TMCM0960.ENUMs.VERSION_FORMAT_BUILD: self.get_version_build
        }.get(request.commandType)

        if(func):
            reply = func(request, reply)
        else:
            reply.status = TMCL_Status.WRONG_TYPE
        return reply

    def get_version_ascii(self, request, reply):
        self.__logger.debug("get_version_ascii")
        reply_data = bytearray(1) + self.__version_string.encode("ascii")
        reply_data[0] = self.__host_address
        reply = TMCL_Reply.from_buffer(reply_data)
        reply.special = True
        return reply

    def get_version_binary(self, request, reply):
        self.__logger.debug("get_version_binary")
        version_module_high = int(self.__version_string[0:2])
        version_module_low = int(self.__version_string[2:4])
        version_fw_high = int(self.__version_string[5:6])
        version_fw_low = int(self.__version_string[6:8])
        reply.value = struct.unpack(">I", struct.pack("BBBB", version_module_high, version_module_low, version_fw_high, version_fw_low))[0]
        return reply

    def get_version_build(self, request, reply):
        self.__logger.debug("get_version_build")
        reply.value = self.__build_version
        return reply

    def set_axis_parameter(self, request, reply):
        self.__logger.debug("set_axis_parameter")
        if(request.motorBank < len(self.ap)):
            if(request.commandType in self.ap[request.motorBank]):
                reply.value = self.ap[request.motorBank][request.commandType] = request.value
            else:
                reply.status = TMCL_Status.WRONG_TYPE
        else:
            reply.status = TMCL_Status.WRONG_TYPE
        return reply

    def get_axis_parameter(self, request, reply):
        self.__logger.debug("get_axis_parameter")
        if(request.motorBank < len(self.ap)):
            if(request.commandType in self.ap[request.motorBank]):
                reply.value = self.ap[request.motorBank][request.commandType]
            else:
                reply.status = TMCL_Status.WRONG_TYPE
        else:
            reply.status = TMCL_Status.WRONG_TYPE
        return reply

    def set_global_parameter(self, request, reply):
        self.__logger.debug("set_global_parameter")
        if(request.commandType == self.GPs.controlHost):
            reply.value = self.__host_address = request.value
        elif(request.commandType == self.GPs.controlModule):
            reply.value = self.__module_address = request.value
        elif(request.commandType == self.GPs.loggingEnabled):
            PyTrinamicMicro.set_logging_enabled(not(request.value == 0))
            reply.value = 1 if PyTrinamicMicro.logging_enabled else 0
        else:
            if(request.commandType in self.gp):
                reply.value = self.gp[request.commandType] = request.value
            else:
                reply.status = TMCL_Status.WRONG_TYPE
        return reply

    def get_global_parameter(self, request, reply):
        self.__logger.debug("get_global_parameter")
        if(request.commandType == self.GPs.controlHost):
            reply.value = self.__host_address
        elif(request.commandType == self.GPs.controlModule):
            reply.value = self.__module_address
        elif(request.commandType == self.GPs.loggingEnabled):
            reply.value = 1 if PyTrinamicMicro.logging_enabled else 0
        else:
            if(request.commandType in self.gp):
                reply.value = self.gp[request.commandType]
            else:
                reply.status = TMCL_Status.WRONG_TYPE
        return reply

    def stop(self, request, reply):
        self.__logger.debug("stop")
        self.status.stop = True
        return reply

    def subscript(self, request, reply):
        self.__logger.debug("subscript")
        func = {
            TMCM0960.ENUMs.SUBSCRIPT_METHOD_EXECUTE: self.subscript_execute,
            TMCM0960.ENUMs.SUBSCRIPT_METHOD_APPEND: self.subscript_append,
            TMCM0960.ENUMs.SUBSCRIPT_METHOD_CLEAR: self.subscript_clear
        }.get(request.commandType)

        if(func):
            reply = func(request, reply)
        else:
            reply.status = TMCL_Status.WRONG_TYPE
        return reply

    def subscript_execute(self, request, reply):
        self.__logger.debug("subscript_execute")
        exec(open(self.__subscript).read())
        return reply

    def subscript_append(self, request, reply):
        self.__logger.debug("subscript_append")
        self.__subscript += struct.pack(">I", request.value).decode("ascii")
        self.__logger.debug("Subscript: {}".format(self.__subscript))
        return reply

    def subscript_clear(self, request, reply):
        self.__logger.debug("subscript_clear")
        self.__subscript = ""
        return reply


class TMCL_Slave_Bridge(TMCL_Slave):

    def __init__(self, module_address=3, host_address=2, version_string="0960V100", build_version=0):
        super().__init__(module_address, host_address, version_string, build_version)
