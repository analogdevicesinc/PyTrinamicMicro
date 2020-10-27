'''
Created on 05.10.2020

@author: LK
'''


from PyTrinamicMicro.connections.uart_tmcl_interface import uart_tmcl_interface
from pyb import UART
from pyb import Pin


class rs485_tmcl_interface(uart_tmcl_interface):

    def __init__(self, port=4, data_rate=9600, host_id=2, module_id=1, debug=False):
        super().__init__(port, data_rate, host_id, module_id, debug)

        self.__dir = Pin(Pin.cpu.B1, Pin.OUT_PP)

    def _send(self, hostID, moduleID, data):
        buf = self.__dir.value()
        self.__dir.high()
        super()._send(hostID, moduleID, data)
        self.__dir.value(buf)

    def _recv(self, hostID, moduleID):
        buf = self.__dir.value()
        self.__dir.low()
        read = super()._recv(hostID, moduleID)
        self.__dir.value(buf)

        return read

    @staticmethod
    def list():
        return [4]
