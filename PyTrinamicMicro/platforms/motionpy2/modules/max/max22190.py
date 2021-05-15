'''
This file implements a basic class for using the MAX22190 in SPI Mode 1. 
For further details refer to the data sheet.
Created on 25.02.2021

@author: JH
'''

from pyb import Pin, SPI
from PyTrinamicMicro.platforms.motionpy2.connections.spi_ic_interface import spi_ic_interface
import struct
import time
import logging
logger = logging.getLogger(__name__)

class MAX22190:
    '''
    This class provides basic functions to use the MAX22190 with mode 1 spi.
    For further details refer to the data sheet.
    '''

    MAX22190_WIRE_BREAK         = 0x00
    MAX22190_DIGITAL_INPUT      = 0x02
    MAX22190_FAULT_1            = 0x04
    MAX22190_FILTER_IN_1        = 0x06
    MAX22190_FILTER_IN_2        = 0x08
    MAX22190_FILTER_IN_3        = 0x0A
    MAX22190_FILTER_IN_4        = 0x0C
    MAX22190_FILTER_IN_5        = 0x0E
    MAX22190_FILTER_IN_6        = 0x10
    MAX22190_FILTER_IN_7        = 0x12
    MAX22190_FILTER_IN_8        = 0x14
    MAX22190_CONFIGURATION      = 0x18
    MAX22190_INPUT_ENABLE       = 0x1A
    MAX22190_FAULT_2            = 0x1C
    MAX22190_FAULT_2_ENABLES    = 0x1E
    MAX22190_GPO                = 0x22
    MAX22190_FAULT_1_ENABLES    = 0x24
    MAX22190_NO_OP              = 0x26

    def __init__(self, cs = Pin.cpu.C0, spi = 1, fault_pin =  Pin.cpu.C1, ready_pin =  Pin.cpu.A13, latch_pin= Pin.cpu.A14):
        self.__SPI = spi_ic_interface(spi=SPI(spi, SPI.MASTER, baudrate=1000, polarity=0, phase=0), cs=cs)
        self.READY  =   Pin(ready_pin, Pin.IN)
        self.FAULT  =   Pin(fault_pin, Pin.IN)
        self.LATCH  =   Pin(latch_pin, Pin.OUT_PP)
        while(self.READY.value() == 1):
            time.sleep(0.1)
        self.set_latch_pin(1)    

    def build_byte_array(self, reg, data = 0x00, rw = 0):
        """returns bytearray with addr, read/write and data, ready to send"""
        bits = str(rw)+ "{:08b}".format((reg)<<1,8)[:7]+"{:08b}".format(data)
        return bytearray(struct.pack("BB",int(bits[:8],2),int(bits[8:],2)))

    def bin_from_recv(self, buf):
        """returns 0/1 string equivalent from inserted send/receive bytearray of length 2"""
        return '{:08b}'.format(buf[0])+" "+'{:08b}'.format(buf[1])

    def read_write(self,buf_send):
        """writing data to spi provided as bytearray returns full receive as bytearray"""
        buf_recv = buf_send
        self.__SPI.send_recv(buf_send, buf_recv)
        return buf_recv

    def read_write_register(self, register, rw = 0 , data = 0x00):
        """read/write data provided as 0/1 string returns received bytearray """
        buf = self.build_byte_array(register, data , rw)
        buf_recv = self.read_write(buf)
        return buf_recv[1]

    def get_digital_input_states(self):
        """ returns list of input states """
        buf = self.build_byte_array(self.MAX22190_DIGITAL_INPUT)
        buf_recv = self.read_write(buf)
        io = list()
        io = [int(x) for x in '{:08b}'.format(buf_recv[1])]
        return io

    def get_wire_break_states(self):
        """ returns list of wire_break states """
        buf = self.build_byte_array(self.MAX22190_WIRE_BREAK)
        buf_recv = self.read_write(buf)
        io = list()
        io = [int(x) for x in '{:08b}'.format(buf_recv[1])]
        return io

    def get_fault_pin(self):
        return not self.FAULT.value()

    def get_ready_pin(self):
        return not self.READY.value()

    def get_latch_pin(self):
         return not self.LATCH.value()

    def set_latch_pin(self,value):
        return self.LATCH.value(value)