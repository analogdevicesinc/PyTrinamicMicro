################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
Created on 06.10.2020

@author: LK
'''


from PyTrinamicMicro.connections.tmcl_module_interface import tmcl_module_interface
from PyTrinamicMicro.connections.tmcl_host_interface import tmcl_host_interface
from pyb import USB_VCP
import micropython

class usb_vcp_tmcl_interface(tmcl_module_interface, tmcl_host_interface):

    def __init__(self, port=0, data_rate=None, host_id=2, module_id=1, debug=False):
        del data_rate
        tmcl_module_interface.__init__(self, host_id, module_id, debug)
        tmcl_host_interface.__init__(self, host_id, module_id, debug)

        self.__vcp = USB_VCP(port)
        self.__vcp.init()
        self.__vcp.setinterrupt(-1)
        micropython.kbd_intr(-1)

    def __enter__(self):
        return self

    def __exit__(self, exitType, value, traceback):
        del exitType, value, traceback
        self.close()

    def close(self):
        self.__vcp.setinterrupt(3)
        micropython.kbd_intr(3)
        self.__vcp.close()
        return 0

    def data_available(self, hostID, moduleID):
        del hostID, moduleID
        return self.__vcp.any()

    def _send(self, hostID, moduleID, data):
        del hostID, moduleID

        self.__vcp.write(data)

    def _recv(self, hostID, moduleID):
        del hostID, moduleID

        read = bytearray(0)
        while(len(read) < 9):
            read += self.__vcp.read(9)
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
    def available_ports():
        return set([0])
