'''
Created on 05.10.2020

@author: LK
'''
from pyb import Pin, SPI

class spi_ic_interface(object):

    def __init__(self, spi=SPI(1, SPI.MASTER, baudrate=10000, polarity=1, phase=1), cs=Pin.cpu.A4):
        self.__spi = spi
        self.__cs = Pin(cs, Pin.OUT_PP)

    def send(self, buf):
        self.__cs.low()
        self.__spi.send(buf)
        self.__cs.high()

    def send_recv(self, buf_send, buf_recv):
        self.__cs.low()
        self.__spi.send_recv(buf_send, buf_recv)
        self.__cs.high()
