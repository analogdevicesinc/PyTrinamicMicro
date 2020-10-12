'''
Created on 05.10.2020

@author: LK
'''

from PyTrinamic.connections.tmcl_interface import tmcl_interface
from PyTrinamicMicro.connections.tmcl_host_interface import tmcl_host_interface
from pyb import CAN
from pyb import Pin
import struct

# CAN transceiver modes
class CanMode(object):
    pass
class CanModeNormal(CanMode):
    pass
class CanModeSilent(CanMode):
    pass
class CanModeOff(CanMode):
    pass

class can_tmcl_interface(tmcl_interface, tmcl_host_interface):
    def __init__(self, can_mode=CanModeNormal(), hostID=2, moduleID=1, debug=False):
        tmcl_interface.__init__(self, hostID, moduleID, debug)
        tmcl_host_interface.__init__(self, hostID, moduleID, debug)

        self.__silent = Pin(Pin.cpu.B14, Pin.OUT_PP)
        self.__mode = can_mode
        self.__flag_recv = False

        self.__set_mode()

        CAN.initfilterbanks(14)

        self.__can = CAN(2, CAN.NORMAL)
        # PCLK1 = 42 MHz, Module_Bitrate = 1000 kBit/s
        # With prescaler = 3, bs1 = 11, bs2 = 2
        # Sample point at 85.7 %, accuracy = 100 %
        self.__can.init(CAN.NORMAL, prescaler=3, bs1=11, bs2=2, auto_restart=True)
        self.__can.setfilter(0, CAN.LIST16, 0, (hostID, hostID, hostID, hostID))
        self.__can.rxcallback(0, self.__callback_recv)

    def __enter__(self):
        return self

    def __exit__(self, exitType, value, traceback):
        del exitType, value, traceback
        self.close()

    def close(self):
        pass

    def data_available(self, hostID, moduleID):
        del hostID, moduleID
        return self.__can.any(0)

    def _send(self, hostID, moduleID, data):
        del hostID, moduleID

        self.__can.send(data[1:], data[0])

    def __callback_recv(self, bus, reason):
        if(reason != 0):
            pass
        self.__flag_recv = True

    def _recv(self, hostID, moduleID):
        del hostID, moduleID

        while(not(self.__flag_recv)):
            pass
        self.__flag_recv = False
        received = self.__can.recv(0, timeout=1000)
        read = struct.pack("B", received[0]) + received[3]

        return read

    def printInfo(self):
        pass

    def enableDebug(self, enable):
        self._debug = enable

    def set_mode(self, mode):
        self.__mode = mode
        self.__set_mode()

    def get_mode(self):
        return self.__mode

    def __set_mode(self):
        if(isinstance(self.__mode, CanModeNormal)):
            self.__silent.low()
        elif(isinstance(self.__mode, CanModeSilent)):
            self.__silent.high()
        elif(isinstance(self.__mode, CanModeOff)):
            pass # Not supported by TJA1051T/3

    def get_can(self):
        return self.__can

    @staticmethod
    def supportsTMCL():
        return True

    @staticmethod
    def supportsCANopen():
        return False

    @staticmethod
    def list():
        return []
