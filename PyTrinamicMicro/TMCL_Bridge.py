'''
Created on 07.10.2020

@author: LK
'''

from PyTrinamicMicro.connections.tmcl_host_interface import tmcl_host_interface
from PyTrinamic.TMCL import TMCL_Request, TMCL_Reply

class TMCL_Bridge(object):
    def __init__(self, host_connection, module_connection):
        self.__host = host_connection
        self.__module = module_connection
    def process(self, request_callback=None, reply_callback=None):
        '''
        1. Receive request from host
        2. Send request to module
        3. Receive reply from module
        4. Send reply to host
        '''
        request = self.receive_request()
        if(request_callback):
            request = request_callback(request)
        self.send_request(request)
        reply = self.receive_reply()
        if(reply_callback):
            reply = reply_callback(reply)
        self.send_reply(reply)
    def receive_request(self):
        return self.__host.receive_request()
    def send_request(self, request):
        self.__module._send(self.__module._HOST_ID, self.__module._MODULE_ID, request.toBuffer())
    def receive_reply(self):
        return TMCL_Reply(reply_data=self.__module._recv(self.__module._HOST_ID, self.__module._MODULE_ID))
    def send_reply(self, reply):
        self.__host.send_reply(reply)
