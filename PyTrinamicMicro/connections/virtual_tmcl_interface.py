'''
Created on 18.12.2020

@author: LK
'''


from PyTrinamic.connections.tmcl_interface import tmcl_interface
from PyTrinamicMicro.connections.tmcl_host_interface import tmcl_host_interface


class virtual_tmcl_interface(tmcl_interface, tmcl_host_interface):

    def __init__(self, port=None, data_rate=None, host_id=2, module_id=1, debug=False):
        tmcl_interface.__init__(self, host_id, module_id, debug)
        tmcl_host_interface.__init__(self, host_id, module_id, debug)

        self.__buffer = bytearray()

    def __enter__(self):
        return self

    def __exit__(self, exitType, value, traceback):
        del exitType, value, traceback
        self.close()

    def close(self):
        return 0

    def data_available(self, hostID=None, moduleID=None):
        del hostID, moduleID
        return bool(self.__buffer)

    def _send(self, hostID, moduleID, data):
        del hostID, moduleID

        self.__buffer += data

    def _recv(self, hostID, moduleID):
        del hostID, moduleID

        read = self.__buffer[0:9]
        self.__buffer = self.__buffer[9:]

        return read

    def printInfo(self):
        pass

    def enableDebug(self, enable):
        self._debug = enable

    @staticmethod
    def supportsTMCL():
        return True

    @staticmethod
    def supportsCANopen():
        return False

    @staticmethod
    def available_ports():
        return set([0])
