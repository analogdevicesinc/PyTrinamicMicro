'''
This file implements a basic class for using the MAX14912 in Command mode SPI. (CMND = HIGH && SRIAL = HIGH)
For further details refer to the data sheet.

Created on 15.02.2021

@author: JH
'''

from pyb import Pin, SPI
from PyTrinamicMicro.platforms.motionpy1.connections.spi_ic_interface import spi_ic_interface
import struct
import logging
logger = logging.getLogger(__name__)

class MAX14912:
    '''
    This class provides basic functions to use the MAX14912 with command mode spi.
    For further details refer to the data sheet.
    '''

    MAX14912_SET_OUT_STATE_CMD =0x00
    MAX14912_SET_HSPP_MODE_CMD =0x01
    MAX14912_SET_OL_DETECT_CMD =0x02
    MAX14912_SET_CONFIG__CMD   =0x03
    MAX14912_READ_REGISTER_CMD =0x20
    MAX14912_RT_STATUS_CMD     =0x30

    MAX14912_REG_SWITCH_DRIVER_SETTINGS         = 0x00
    MAX14912_PUSH_PULL_HIGH_SIDE_CONFIG         = 0x01
    MAX14912_OPEN_LOAD_DETECT_ENABLE            = 0x02
    MAX14912_WATCHDOG_CONFIG_AND_CH_PARAL       = 0x03
    MAX14912_PER_CHANNEL_OPEN_LOAD_COND         = 0x04
    MAX14912_PER_CHANNEL_THERMAL_SHUTDOWN       = 0x05
    MAX14912_GLOBAL_FAULTS                      = 0x06
    MAX14912_OUT_OVERVOLT_DETECT_OR_SLOW_MODE   = 0x07

    def __init__(self, pin_cs = Pin.cpu.C0, spi = 1,  pin_fltr = Pin.cpu.A13, pin_cmd =Pin.cpu.C1):
        FLTR  = Pin(pin_fltr, Pin.OUT_PP)
        CMND  = Pin(pin_cmd, Pin.OUT_PP)
        FLTR.high()
        CMND.high()
        self.__SPI = spi_ic_interface(spi=SPI(spi, SPI.MASTER, baudrate=5000, polarity=0, phase=0), cs=pin_cs)

        self.outputs = 0x00
        buf = self.build_byte_array(self.MAX14912_SET_OUT_STATE_CMD,"00000000")
        self.__SPI.send_recv(buf,buf)

    def build_byte_array(self, cmd, data = "00000000", cl_fault = 0):
        """returns bytearray with addr, read/write and data, ready to send"""
        bits = str(cl_fault)+ "{:08b}".format((cmd)<<1,8)[:7]+data
        return bytearray(struct.pack("BB",int(bits[:8],2),int(bits[8:],2)))

    def bin_from_recv(self, buf):
        """returns 0/1 string equivalent from inserted send/receive bytearray of length 2"""
        return '{:08b}'.format(buf[0])+" "+'{:08b}'.format(buf[1])

    def write(self,buf_send):
        """writing data provided as 0/1 string to addr. returns full receive as bytearray"""
        buf_recv = buf_send
        self.__SPI.send_recv(buf_send, buf_recv)
        return buf_recv

    def set_output(self, nr, value = "0"):
        '''Set the Output nr(0-7) to HIGH(1) or LOW(0) '''
        bits = list()
        bits = [int(x) for x in '{:08b}'.format(self.outputs)]
        bits[7-nr] = value
        self.outputs = int(''.join(str(e) for e in bits),2)
        buf = self.build_byte_array(self.MAX14912_SET_OUT_STATE_CMD, str('{:08b}'.format(self.outputs)))
        self.write(buf)

    def write_register(self,reg,value):
        buf = self.build_byte_array(self.MAX14912_SET_OUT_STATE_CMD, str('{:08b}'.format(self.outputs)))
        self.write(buf)
        '{:08b}'.format(buf[0])
        return

    def read_register(self,register, cl_fault_regs = 0):
        """Reads out register and returns received bytearray"""
        buf = self.build_byte_array(self.MAX14912_READ_REGISTER_CMD,'{:08b}'.format(register) ,cl_fault_regs)
        self.write(buf)
        buf_recv = self.write(buf)
        return '{:08b}'.format(buf_recv[0])

    def read_status(self, cl_fault_regs = 0):
        """Reads out status and returns received bytearray"""
        buf = self.build_byte_array(self.MAX14912_RT_STATUS_CMD, "00000000", cl_fault_regs)
        self.write(buf)
        buf_recv = self.write(buf)
        return buf_recv
