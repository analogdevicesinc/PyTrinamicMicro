'''
Created on 05.10.2020

@author: LK
'''

import struct
from pyb import UART
import stm

class uart_ic_interface(object):

    def __init__(self, port=3, data_rate=9600, single_wire=False):
        self.__uart = UART(port, data_rate)
        self.__uart.init(baudrate=data_rate, bits=8, parity=None, stop=1, timeout=1000, timeout_char=1000)
        self.__single_wire = single_wire
        if(self.__single_wire and (port==3)):
            stm.mem32[stm.GPIOB + stm.GPIO_OTYPER] |= (1 << 10) # Set open drain
            stm.mem32[stm.GPIOB + stm.GPIO_PUPDR] &= ~(1 << 21)
            stm.mem32[stm.GPIOB + stm.GPIO_PUPDR] &= ~(1 << 20) # Set nopull
            stm.mem32[stm.USART3 + stm.USART_CR3] |= 0b1000 # set HDSEL
            stm.mem32[stm.GPIOB + stm.GPIO_PUPDR] &= ~(1 << 23)
            stm.mem32[stm.GPIOB + stm.GPIO_PUPDR] |= (1 << 22) # Set pullup

    def send(self, buf):
        print("send: {}".format(buf))
        self.__uart.write(buf)
        if(self.__single_wire):
            self.__uart.read(len(buf))

    def recv(self, nbytes):
        buf = self.__uart.read(nbytes)
        print("recv: {}".format(buf))
        return buf
