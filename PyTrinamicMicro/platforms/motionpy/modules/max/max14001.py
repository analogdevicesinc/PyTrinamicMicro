'''
This file implements a basic class for the MAX14001 ic as well as 
a basic implementaion to use the module MAX14001PMB.

Created on 27.01.2020

@author: JH
'''

from pyb import Pin, SPI
from PyTrinamicMicro.platforms.motionpy.connections.spi_ic_interface import spi_ic_interface
import time
import struct

class  MAX14001(object):
    '''This class provides basic functions to use the MAX14001, for further details refer to the data sheet.'''
    MAX14001_ADC_adr=0x00       #ADC R 
    MAX14001_FADC_adr=0x01      #Filtered ADC R 
    MAX14001_FLAGS_adr= 0x02    #Error Flags R 
    MAX14001_FLTEN_adr=0x03     #FAULT Enable RW
    MAX14001_THL_adr=0x04       #Lower Threshold RW 
    MAX14001_THU_adr=0x05       #Upper Threshold RW 
    MAX14001_INRR_adr=0x06      #Inrush Reset RW 
    MAX14001_INRT_adr=0x07      #Inrush Trigger RW 
    MAX14001_INRP_adr=0x08      #Inrush Pulse RW
    MAX14001_CFG_adr=0x09       #Configuration RW 
    MAX14001_ENBL_adr=0x0a      #Enable RW 
    MAX14001_WVR_adr=0x0c       #Write Verification RW 
    #verification registers
    MAX14001_FLTV_adr=0x13      # FAULT Enable verification RW 
    MAX14001_THLV_adr=0x14      #Lower Threshold verification RW 
    MAX14001_THUV_adr=0x15      #Upper Threshold verification RW
    MAX14001_INRRV_adr=0x16     #Inrush Reset verification RW 
    MAX14001_INRTV_adr=0x17     #Inrush Trigger verification RW 
    MAX14001_INRPV_adr=0x18     #Inrush Pulse verification RW
    MAX14001_CFGV_adr=0x19      #Configuration verification RW
    MAX14001_ENBLV_adr=0x1a     #Enable verification RW 

    def __init__(self, cs = Pin.cpu.A4):
        self.__SPI = spi_ic_interface(spi=SPI(1, SPI.MASTER, baudrate=5000, polarity=0, phase=0), cs=cs)
    
    def rev(self, s):
        """returns inverse of string s"""       
        return "" if not(s) else self.rev(s[1::])+s[0]

    def build_byte_array(self,addr, rw, data = "0000000000"):
        """returns bytearray with addr, read/write and data"""
        bits = "{:08b}".format((addr)<<3,8)[:5]+str(rw)+data
        inv_bits = self.rev(bits)
        return bytearray(struct.pack("BB",int(inv_bits[:8],2),int(inv_bits[8:],2)))

    def bin_from_recv(self,buf):
        """returns 0/1 string equivalent from send/receive buf"""
        return '{:08b}'.format(buf[0])+'{:08b}'.format(buf[1])

    def data_from_recv(self,buf):
        """extracts data from receive, returns string"""
        return self.rev(self.bin_from_recv(buf))[6:]

    def int_from_data(self,data):
        """returns integer from 0/1 string"""
        return int(data,2)

    def read(self, addr):
        """sending read request and returns 10bits 0/1 string"""
        buf = self.build_byte_array(0x01,0)
        self.__SPI.send_recv(buf,buf)
        return self.data_from_recv(buf)

    def read_full_response(self, addr):
        """sending read request and returns 10bits 0/1 string"""
        buf = self.build_byte_array(0x01,0)
        self.__SPI.send_recv(buf,buf)
        return self.bin_from_recv(buf)
       
    def write(self, addr, data = "0000000000"):
        """writing data provided as 0/1 string to addr. returns full receive as string"""
        buf = self.build_byte_array(0x01,1, data)
        self.__SPI.send_recv(buf,buf)
        return self.bin_from_recv(buf)



class  MAX14001PMB(object):
    '''This class provides basic functions to use the MAX14001PMB, for further details refer to the data sheet.'''
    VOLT_FACTOR = 0.666
    VOLT_OFFSET = 2.664
    CURRENT_FACTOR = -0.0115 
    CURRENT_OFFSET = 0.13

    def __init__(self,  csU = Pin.cpu.C0,  csI = Pin.cpu.A4):
        self.voltADC = MAX14001(Pin.cpu.C0)
        self.currentADC = MAX14001(Pin.cpu.A4)

    def getVoltage(self, filtered = True):
        if filtered == True:
            return self.VOLT_FACTOR*(int(self.voltADC.read(self.voltADC.MAX14001_FADC_adr),2)-512)-self.VOLT_OFFSET
        else:
            return self.VOLT_FACTOR*(int(self.voltADC.read(self.voltADC.MAX14001_ADC_adr),2)-512)-self.VOLT_OFFSET

    def getCurrent(self, filtered = True):
        if filtered == True:
            return self.CURRENT_FACTOR*(int(self.currentADC.read(self.currentADC.MAX14001_FADC_adr),2)-512)-self.CURRENT_OFFSET
        else:
            return self.CURRENT_FACTOR*(int(self.currentADC.read(self.currentADC.MAX14001_ADC_adr),2)-512)-self.CURRENT_OFFSET

