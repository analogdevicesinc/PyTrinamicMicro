'''
Created on 06.10.2020

@author: LK
'''

from PyTrinamic.connections.tmcl_interface import tmcl_interface
from pyb import USB_VCP

class usb_vcp_tmcl_interface(tmcl_interface):
    def __init__(self, id=0, hostID=2, moduleID=1, debug=False):
        super().__init__(hostID, moduleID, debug)

        self.__vcp = USB_VCP(id)
        self.__vcp.init()
        self.__vcp.setinterrupt(-1)

    def __enter__(self):
        return self

    def __exit__(self, exitType, value, traceback):
        del exitType, value, traceback
        self.close()

    def close(self):
        self.__vcp.close()
        return 0

    def data_available(self, hostID, moduleID):
        del hostID, moduleID
        return self.__vcp.any()

    def send(self, hostID, moduleID, data):
        del hostID, moduleID

        self.__vcp.write(data)

    def receive(self, hostID, moduleID):
        del hostID, moduleID

        read = bytearray(0)
        while(len(read) < 9):
            read = self.__vcp.read(9)
            if(not(read)):
                read = bytearray(0)

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
    def list():
        return []
