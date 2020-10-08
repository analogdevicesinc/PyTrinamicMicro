'''
Created on 07.10.2020

@author: LK
'''

from PyTrinamicMicro.connections.tmcl_host_interface import tmcl_host_interface
from PyTrinamicMicro.TMCL_Slave import TMCL_Slave_Bridge
from PyTrinamic.TMCL import TMCL_Request, TMCL_Reply

class TMCL_Bridge(object):
    '''
    Initialize the TMCL bridge.

    Parameters:
        host_connection: tmcl_interface to the main host.
        module_connection: tmcl_interface to the module.
        module_id: module ID to be used in control mode.
        host_id: host ID to be used in control mode.
    '''
    def __init__(self, host_connection, module_connection, module_id=3, host_id=2):
        self.__host = host_connection
        self.__module = module_connection
        self.__slave = TMCL_Slave_Bridge(module_id, host_id)
    def process(self, request_callback=None, reply_callback=None):
        '''
        1. Receive request from host
        2. Send request to module
        3. Receive reply from module
        4. Send reply to host
        '''
        if(self.__host.request_available()):
            request = self.receive_request()
            if(self.__slave.filter(request)): # Control request
                reply = self.__slave.handle_request(request)
                self.__host.send_reply(reply)
            else: # Passthrough request
                if(request_callback):
                    request = request_callback(request)
                self.send_request(request)
                reply = self.receive_reply()
                if(reply_callback):
                    reply = reply_callback(reply)
                self.send_reply(reply)
        return self.__slave.get_status().stop
    def receive_request(self):
        return self.__host.receive_request()
    def send_request(self, request):
        self.__module.send(self.__module._HOST_ID, self.__module._MODULE_ID, request.toBuffer())
    def receive_reply(self):
        return TMCL_Reply(reply_data=self.__module.receive(self.__module._HOST_ID, self.__module._MODULE_ID))
    def send_reply(self, reply):
        self.__host.send_reply(reply)
