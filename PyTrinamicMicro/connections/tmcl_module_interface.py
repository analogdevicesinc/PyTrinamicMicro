'''
Interface to the TMCL module.

Created on 05.02.2021

@author: LK
'''

from PyTrinamic.connections.tmcl_interface import tmcl_interface

class tmcl_module_interface(tmcl_interface):

    def data_available(self, host_id=None, module_id=None):
        raise NotImplementedError()

    def reply_available(self, host_id=None, module_id=None):
        return self.data_available(host_id, module_id)
