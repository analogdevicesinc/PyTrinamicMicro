'''
Created on 30.12.2018

@author: ED
'''

from PyTMCMicro.Connection.TMCL import TMCL_Connection
from pyb import UART

class UART_Connection(TMCL_Connection):
    """
    Opens a serial TMCL connection
    """
    def __init__(self, baudrate=9600, hostID=2, moduleID=1, debug=False):
        super().__init__(hostID, moduleID, debug)

        self.__uart = UART(3, baudrate)
        self.__uart.init(baudrate=baudrate, bits=8, parity=None, stop=1, timeout=10000, timeout_char=10000)

    def __enter__(self):
        return self

    def __exit__(self, exitType, value, traceback):
        """
        Close the connection at the end of a with-statement block.
        """
        del exitType, value, traceback
        self.close()

    def close(self):
        self.__uart.deinit()
        return 0;

    def _send(self, hostID, moduleID, data):
        """
            Send the bytearray parameter [data].

            This is a required override function for using the tmcl_interface
            class.
        """
        del hostID, moduleID

        self.__uart.write(data)

    def _recv(self, hostID, moduleID):
        """
            Read 9 bytes and return them as a bytearray.

            This is a required override function for using the tmcl_interface
            class.
        """
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
        """
            Return a list of available connection ports as a list of strings.

            This function is required for using this interface with the
            connection manager.
        """
        return []
