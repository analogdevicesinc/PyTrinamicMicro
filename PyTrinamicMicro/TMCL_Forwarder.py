'''
Created on 07.10.2020

@author: LK
'''

from PyTrinamicMicro.connections.tmcl_host_interface import tmcl_host_interface
from PyTrinamic.TMCL import TMCL_Reply

class TMCL_Forwarder(object):
    def __init__(self, host_connection, module_connection):
        self.__host = host_connection
        self.__module = module_connection
    def forward(self):
        '''
        1. Receive request from host
        2. Send request to module
        3. Receive reply from module
        4. Send reply to host
        '''
        request = self.__host.receive_request()
        self.__module._send(self.__module._HOST_ID, self.__module._MODULE_ID, request.toBuffer())
        reply = self.__module._recv(self.__module._HOST_ID, self.__module._MODULE_ID)
        self.__host.send_reply(TMCL_Reply(reply_data=reply))
