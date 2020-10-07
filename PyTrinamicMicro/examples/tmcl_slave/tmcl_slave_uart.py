'''
Act as TMCL slave over UART.

Created on 06.10.2020

@author: LK
'''

# Imports
from PyTrinamicMicro.connections.tmcl_host_interface import tmcl_host_interface
from PyTrinamicMicro.connections.uart_tmcl_interface import uart_tmcl_interface
from PyTrinamic.TMCL import TMCL_Request, TMCL_Reply, TMCL_Status, TMCL_Command, TMCL_Version_Format
import struct

# Constants
MODULE_ADDRESS = 1
HOST_ADDRESS = 2
MODULE_ID_STRING = "0012"
VERSION_STRING = MODULE_ID_STRING + "V308"
BUILD_VERSION = 0

# Functions

def get_version(request, reply):
    func = {
        TMCL_Version_Format.ASCII: get_version_ascii,
        TMCL_Version_Format.BINARY: get_version_binary,
        TMCL_Version_Format.BUILD: get_version_build
    }.get(request.commandType)

    if(func):
        reply = func(request, reply)
    else:
        reply.status = TMCL_Status.WRONG_TYPE
    return reply

def get_version_ascii(request, reply):
    reply_data = bytearray(1) + VERSION_STRING.encode("ascii")
    reply_data[0] = HOST_ADDRESS
    reply = TMCL_Reply(reply_data=reply_data)
    reply.special = True
    return reply

def get_version_binary(request, reply):
    version_module_high = int(VERSION_STRING[0:2])
    version_module_low = int(VERSION_STRING[2:4])
    version_fw_high = int(VERSION_STRING[5:6])
    version_fw_low = int(VERSION_STRING[6:8])
    reply.value = struct.unpack(">I", struct.pack("BBBB", version_module_high, version_module_low, version_fw_high, version_fw_low))[0]
    return reply

def get_version_build(request, reply):
    reply.value = BUILD_VERSION
    return reply

MAP_COMMAND_FUNCTION = {
    TMCL_Command.GET_FIRMWARE_VERSION: get_version
}

def handle_request(request):
    reply = TMCL_Reply(reply_address=HOST_ADDRESS, module_address=MODULE_ADDRESS, status=TMCL_Status.SUCCESS, command=request.command)

    # Switch command
    command_func = MAP_COMMAND_FUNCTION.get(request.command)
    if(command_func):
        reply = command_func(request, reply)
    else:
        reply.status = TMCL_Status.INVALID_COMMAND

    if(not(reply.special)):
        reply.reply_address = HOST_ADDRESS
        reply.calculate_checksum()

    return reply

# Main program

host = tmcl_host_interface(uart_tmcl_interface())

while(True):
    request = host.receive_request()
    if(not(request.moduleAddress == MODULE_ADDRESS)):
        continue
    reply = handle_request(request)
    host.send_reply(reply)
