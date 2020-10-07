'''
Interface to the TMCL host.
This way, the micropython can be handled as TMCL slave.

Created on 06.10.2020

@author: LK
'''

from PyTrinamic.TMCL import TMCL, TMCL_Request

class tmcl_host_interface(object):
    def __init__(self, interface, host_id=2, module_id=1, debug=False):
        TMCL.validate_host_id(host_id)
        TMCL.validate_module_id(module_id)
        self.__interface = interface
        self.__host_id = host_id
        self.__module_id = module_id
        self.__debug = debug

    def receive_request(self, host_id=None, module_id=None):
        if(not host_id):
            host_id = self.__host_id
        if(not module_id):
            module_id = self.__module_id
        request = TMCL_Request(request_data=self.__interface._recv(module_id, host_id))
        if(self.__debug):
            request.dump()
        return request

    def send_reply(self, reply, host_id=None, module_id=None):
        if(not host_id):
            host_id = self.__host_id
        if(not module_id):
            module_id = self.__module_id
        if(self.__debug):
            reply.dump()
        self.__interface._send(module_id, host_id, reply.toBuffer())
