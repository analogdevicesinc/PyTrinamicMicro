'''
Bridge from UART host to RS232 module.

Created on 07.10.2020

@author: LK
'''

from PyTrinamicMicro.connections.tmcl_host_interface import tmcl_host_interface
from PyTrinamicMicro.connections.can_tmcl_interface import can_tmcl_interface
from PyTrinamicMicro.connections.uart_tmcl_interface import uart_tmcl_interface
from PyTrinamicMicro.TMCL_Bridge import TMCL_Bridge
from PyTrinamic.TMCL import TMCL_Command

request_command = 0

def request_callback(request):
    global request_command
    request_command = request.command
    return request

def reply_callback(reply):
    if(request_command != TMCL_Command.GET_FIRMWARE_VERSION):
        reply.reply_address = 2
        reply.calculate_checksum()
    return reply

bridge = TMCL_Bridge(tmcl_host_interface(uart_tmcl_interface()), can_tmcl_interface())

while(True):
    bridge.process(request_callback=request_callback, reply_callback=reply_callback)
