'''
Interface to the TMCL host.
This way, the micropython can be handled as TMCL slave.

Created on 06.10.2020

@author: LK
'''

from PyTrinamic.TMCL import TMCL, TMCL_Request, TMCL_Reply

class tmcl_host_interface(object):
    def __init__(self, host_id=2, module_id=1, debug=False):
        TMCL.validate_host_id(host_id)
        TMCL.validate_module_id(module_id)
        self.__host_id = host_id
        self.__module_id = module_id
        self.__debug = debug

    def data_available(self):
        raise NotImplementedError("data_available() function is not implemented for this tmcl_host_interface.")

    def _send(self, hostID, moduleID, data):
        raise NotImplementedError("The tmcl_host_interface requires an implementation of the _send() function.")

    def _recv(self, hostID, moduleID):
        raise NotImplementedError("The tmcl_host_interface requires an implementation of the _recv() function.")

    def request_available(self, host_id=None, module_id=None):
        if(not host_id):
            host_id = self.__host_id
        if(not module_id):
            module_id = self.__module_id
        return self.__interface.data_available(host_id, module_id)

    def receive_request(self, host_id=None, module_id=None):
        if(not host_id):
            host_id = self.__host_id
        if(not module_id):
            module_id = self.__module_id
        request = TMCL_Request.from_buffer(self._recv(host_id, module_id))
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
        self._send(module_id, host_id, reply.toBuffer())
