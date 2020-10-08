'''
Created on 07.10.2020

@author: LK
'''

# Imports
from PyTrinamic.TMCL import TMCL_Request, TMCL_Reply, TMCL_Status, TMCL_Command, TMCL_Version_Format
import struct

class TMCL_Slave_Status(object):
    def __init__(self):
        self.stop = False

class TMCL_Slave(object):
    def __init__(self, module_address=1, host_address=2, version_string="0021V100", build_version=0):
        self.__module_address = module_address
        self.__host_address = host_address
        self.__version_string = version_string
        self.__build_version = build_version
        self._status = TMCL_Slave_Status()
    def filter(self, request):
        return (request.moduleAddress == self.__module_address)
    def _get_command_func(self):
        return {
            TMCL_Command.GET_FIRMWARE_VERSION: self.get_version,
            TMCL_Command.SGP: self.set_global_parameter,
            TMCL_Command.GGP: self.get_global_parameter
        }
    def get_status(self):
        return self._status
    def handle_request(self, request):
        reply = TMCL_Reply(reply_address=self.__host_address, module_address=self.__module_address, status=TMCL_Status.SUCCESS, command=request.command)

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
        func = {
            TMCL_Version_Format.ASCII: self.get_version_ascii,
            TMCL_Version_Format.BINARY: self.get_version_binary,
            TMCL_Version_Format.BUILD: self.get_version_build
        }.get(request.commandType)

        if(func):
            reply = func(request, reply)
        else:
            reply.status = TMCL_Status.WRONG_TYPE
        return reply
    def get_version_ascii(self, request, reply):
        reply_data = bytearray(1) + self.__version_string.encode("ascii")
        reply_data[0] = self.__host_address
        reply = TMCL_Reply(reply_data=reply_data)
        reply.special = True
        return reply
    def get_version_binary(self, request, reply):
        version_module_high = int(self.__version_string[0:2])
        version_module_low = int(self.__version_string[2:4])
        version_fw_high = int(self.__version_string[5:6])
        version_fw_low = int(self.__version_string[6:8])
        reply.value = struct.unpack(">I", struct.pack("BBBB", version_module_high, version_module_low, version_fw_high, version_fw_low))[0]
        return reply
    def get_version_build(self, request, reply):
        reply.value = self.__build_version
        return reply
    def set_global_parameter(self, request, reply):
        if(request.commandType == 0):
            reply.value = self.__host_address = request.value
        elif(request.commandType == 1):
            reply.value = self.__module_address = request.value
        else:
            reply.status = TMCL_Status.WRONG_TYPE
        return reply
    def get_global_parameter(self, request, reply):
        if(request.commandType == 0):
            reply.value = self.__host_address
        elif(request.commandType == 1):
            reply.value = self.__module_address
        else:
            reply.status = TMCL_Status.WRONG_TYPE
        return reply

class TMCL_Slave_Bridge(TMCL_Slave):
    class _APs(object):
        pass
    class _ENUMs(object):
        pass
    class _GPs(object):
        controlHost = 0
        controlModule = 1
    def _get_command_func(self):
        command_func = {}
        command_func.update(super()._get_command_func())
        command_func.update({
            TMCL_Command.TMCL_UF0: self.stop
        })
        return command_func
    def stop(self, request, reply):
        self._status.stop = True
        return reply
