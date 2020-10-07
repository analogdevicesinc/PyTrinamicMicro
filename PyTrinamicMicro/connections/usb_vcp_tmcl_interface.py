'''
Created on 06.10.2020

@author: LK
'''

from PyTrinamic.connections.tmcl_interface import tmcl_interface

class usb_vcp_tmcl_interface(tmcl_interface):
    def __init__(self, id=3, baudrate=9600, hostID=2, moduleID=1, debug=False):
        super().__init__(hostID, moduleID, debug)

        self.__uart = UART(id, baudrate)
        self.__uart.init(baudrate=baudrate, bits=8, parity=None, stop=1, timeout=10000, timeout_char=10000)

    def __enter__(self):
        return self

    def __exit__(self, exitType, value, traceback):
        del exitType, value, traceback
        self.close()

    def close(self):
        self.__uart.deinit()
        return 0;

    def _send(self, hostID, moduleID, data):
        del hostID, moduleID

        self.__uart.write(data)

    def _recv(self, hostID, moduleID):
        del hostID, moduleID

        read = self.__uart.read(9)

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
