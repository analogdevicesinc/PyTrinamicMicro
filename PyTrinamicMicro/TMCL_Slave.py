'''
Created on 07.10.2020

@author: LK
'''

# Imports
from PyTrinamic.TMCL import TMCL_Request, TMCL_Reply, TMCL_Status, TMCL_Command, TMCL_Version_Format
import struct

class TMCL_Slave(object):
    def __init__(self, module_address=1, host_address=2, version_string="0012V308", build_version=0):
        self.__module_address = module_address
        self.__host_address = host_address
        self.__version_string = version_string
        self.__build_version = build_version
    def filter(self, request):
        return (request.moduleAddress == self.__module_address)
    def handle_request(self, request):
        reply = TMCL_Reply(reply_address=self.__host_address, module_address=self.__module_address, status=TMCL_Status.SUCCESS, command=request.command)

        # Switch command
        command_func = {
            TMCL_Command.GET_FIRMWARE_VERSION: self.get_version
        }.get(request.command)
        if(command_func):
            reply = command_func(request, reply)
        else:
            reply.status = TMCL_Status.INVALID_COMMAND

        if(not(reply.special)):
            reply.reply_address = self.__host_address
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
