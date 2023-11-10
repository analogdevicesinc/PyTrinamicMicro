################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
This file implements a basic class for the MAX14001 ic as well as 
a basic implementaion to use the module MAX14001PMB.

Created on 27.01.2021

@author: JH
'''

from pyb import Pin, SPI
from PyTrinamicMicro.platforms.motionpy2.connections.spi_ic_interface import spi_ic_interface
import time
import struct

class  MAX14001(object):
    '''This class provides basic functions to use the MAX14001, for further details refer to the data sheet.'''
    MAX14001_ADC_adr=0x00       #ADC R 
    MAX14001_FADC_adr=0x01      #Filtered ADC R 
    MAX14001_FLAGS_adr= 0x02    #Error Flags R 
    MAX14001_FLTEN_adr=0x03     #FAULT Enable R&W
    MAX14001_THL_adr=0x04       #Lower Threshold R&W 
    MAX14001_THU_adr=0x05       #Upper Threshold R&W 
    MAX14001_INRR_adr=0x06      #Inrush Reset R&W 
    MAX14001_INRT_adr=0x07      #Inrush Trigger R&W 
    MAX14001_INRP_adr=0x08      #Inrush Pulse R&W
    MAX14001_CFG_adr=0x09       #Configuration R&W 
    MAX14001_ENBL_adr=0x0a      #Enable R&W 
    MAX14001_ACT_adr=0x0B       #Immediate action register W&C
    MAX14001_WVR_adr=0x0c       #SPI Write Enable R&W 
    #verification registers
    MAX14001_FLTV_adr=0x13      # FAULT Enable verification R&W 
    MAX14001_THLV_adr=0x14      #Lower Threshold verification R&W 
    MAX14001_THUV_adr=0x15      #Upper Threshold verification R&W
    MAX14001_INRRV_adr=0x16     #Inrush Reset verification R&W 
    MAX14001_INRTV_adr=0x17     #Inrush Trigger verification R&W 
    MAX14001_INRPV_adr=0x18     #Inrush Pulse verification R&W
    MAX14001_CFGV_adr=0x19      #Configuration verification R&W
    MAX14001_ENBLV_adr=0x1a     #Enable verification R&W 

    def __init__(self, cs = Pin.cpu.A4, spi= 1, cout = None):
        self.__SPI = spi_ic_interface(spi=SPI(spi, SPI.MASTER, baudrate=10000, polarity=0, phase=0), cs=cs)
        if cout:
            self.__COUT = Pin(cout, Pin.IN)
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
        buf_send = self.build_byte_array(addr,0)
        buf_recv = buf_send
        self.__SPI.send_recv(buf_send,buf_recv)
        self.__SPI.send_recv(buf_send,buf_recv)
        return self.data_from_recv(buf_recv)

    def read_full_response(self, addr):
        """sending read request and returns 10bits 0/1 string"""
        buf_send = self.build_byte_array(addr,0)
        buf_recv = buf_send
        self.__SPI.send_recv(buf_send,buf_recv)
        self.__SPI.send_recv(buf_send,buf_recv)
        return self.bin_from_recv(buf_recv)
       
    def write(self, addr, data = "0000000000"):
        """writing data provided as 0/1 string to addr. returns full receive as string"""
        buf = self.build_byte_array(addr,1, data)
        self.__SPI.send_recv(buf,buf)
        return self.bin_from_recv(buf)

    def enable_write(self, enable):
        """enable register write, set enable to 1 to enable"""
        if enable ==  1:
            self.write(self.MAX14001_WVR_adr, "1010010100")
        else:
            self.write(self.MAX14001_WVR_adr, "0000000000")


    def get_cout(self):
        """returns value of specified pin for comparator (if assigned)"""
        try: 
            return self.__COUT.value()
        except AttributeError:
            return  "Not assigned"  
    
    def write_verification(self):
        """Write the values back to their appropriate verification registers to clear the MV Fault"""
        reg_FLTEN = self.read(self.MAX14001_FLTEN_adr)
        reg_THL = self.read(self.MAX14001_THL_adr)    
        reg_THU = self.read(self.MAX14001_THU_adr)      
        reg_INRR = self.read(self.MAX14001_INRR_adr)    
        reg_INRT = self.read(self.MAX14001_INRT_adr)    
        reg_INRP = self.read(self.MAX14001_INRP_adr)    
        reg_CFG = self.read(self.MAX14001_CFG_adr)   
        reg_ENBL = self.read(self.MAX14001_ENBL_adr)   

        self.enable_write(1)

        self.write(self.MAX14001_FLTV_adr, reg_FLTEN)
        self.write(self.MAX14001_THLV_adr, reg_THL)
        self.write(self.MAX14001_THUV_adr, reg_THU)
        self.write(self.MAX14001_INRRV_adr, reg_INRR)
        self.write(self.MAX14001_INRTV_adr, reg_INRT)
        self.write(self.MAX14001_INRPV_adr, reg_INRP)
        self.write(self.MAX14001_CFGV_adr, reg_CFG)
        self.write(self.MAX14001_ENBLV_adr, reg_ENBL)

        self.enable_write(0)
        
class  MAX14001PMB(object):
    '''This class provides basic functions to use the MAX14001PMB, for further details refer to the data sheet.'''
    VOLT_FACTOR = 0.666
    VOLT_OFFSET = 0
    CURRENT_FACTOR = -0.012
    CURRENT_OFFSET = 0.34
    spi=1
    def __init__(self, **kwargs):
        time.sleep(0.2)
        if "spi" in kwargs:
            spi = kwargs["spi"] 

        if  "pin_cs_volt" in kwargs: 
            if "pin_cout_volt" in kwargs:
                self.voltADC = MAX14001(kwargs["pin_cs_volt"],spi, kwargs["pin_cout_volt"])
            else:
                self.voltADC = MAX14001(kwargs["pin_cs_volt"],spi)
            self.voltADC.enable_write(1)
            self.voltADC.write(self.voltADC.MAX14001_CFG_adr, "0110110011")
            self.voltADC.write(self.voltADC.MAX14001_INRR_adr,"1111111111")
            self.voltADC.enable_write(0)
            self.voltADC.write_verification()

        if  "pin_cs_curr" in kwargs: 
            if "pin_cout_curr" in kwargs:
                self.currentADC = MAX14001(kwargs["pin_cs_curr"],spi, kwargs["pin_cout_curr"])
            else:
                self.currentADC = MAX14001(kwargs["pin_cs_curr"],spi)
            self.currentADC.enable_write(1)
            self.currentADC.write(self.voltADC.MAX14001_CFG_adr, "0110110011")
            self.currentADC.write(self.voltADC.MAX14001_INRR_adr,"1111111111")
            self.currentADC.enable_write(0)
            self.currentADC.write_verification()
        if  "pin_fault" in kwargs:
            self.__Fault =  Pin(kwargs["pin_fault"], Pin.IN)

    def get_voltage(self, filtered = True):
        """returns voltage"""
        try:
            if filtered == True:
                return self.VOLT_FACTOR*(int(self.voltADC.read(self.voltADC.MAX14001_FADC_adr),2)-511)-self.VOLT_OFFSET
            else:
                return self.VOLT_FACTOR*(int(self.voltADC.read(self.voltADC.MAX14001_ADC_adr),2)-511)-self.VOLT_OFFSET
        except AttributeError:
            return "Not assigned" 

    def get_current(self, filtered = True):
        """returns current"""
        try:
            if filtered == True:
                return self.CURRENT_FACTOR*(int(self.currentADC.read(self.currentADC.MAX14001_FADC_adr),2)-511)-self.CURRENT_OFFSET
            else:
                return self.CURRENT_FACTOR*(int(self.currentADC.read(self.currentADC.MAX14001_ADC_adr),2)-511)-self.CURRENT_OFFSET
        except AttributeError:
            return "Not assigned" 

    def get_fault(self):
        """returns status of fault pin if assigned """
        try: 
            return not self.__Fault.value()
        except AttributeError:
            return "Not assigned" 

    def set_cout_volt(self,lower_value, upper_value):
        '''set the threshold for voltage comparator'''
        lower_value_scaled = (lower_value+self.VOLT_OFFSET)/self.VOLT_FACTOR + 511
        upper_value_scaled = (upper_value+self.VOLT_OFFSET)/self.VOLT_FACTOR + 511
        self.voltADC.enable_write(1)
        self.voltADC.write(self.voltADC.MAX14001_THL_adr, "{:010b}".format(round(lower_value_scaled))[:10])
        self.voltADC.write(self.voltADC.MAX14001_THU_adr, "{:010b}".format(round(upper_value_scaled))[:10])
        self.voltADC.write_verification()
        self.voltADC.enable_write(0)

    def set_cout_curr(self,lower_value, upper_value):
        '''set the threshold for current comparator'''
        upper_value_scaled = (lower_value+self.CURRENT_OFFSET)/self.CURRENT_FACTOR + 511
        lower_value_scaled = (upper_value+self.CURRENT_OFFSET)/self.CURRENT_FACTOR + 511 
        self.currentADC.enable_write(1)
        self.currentADC.write(self.currentADC.MAX14001_THL_adr, "{:010b}".format(round(lower_value_scaled))[:10])
        self.currentADC.write(self.currentADC.MAX14001_THU_adr, "{:010b}".format(round(upper_value_scaled))[:10])
        self.currentADC.write_verification()
        self.currentADC.enable_write(0)
    def get_cout_volt(self):
        """returns value of specified pin for voltage comparator (if assigned)"""
        return bool(self.voltADC.get_cout())
    def get_cout_curr(self):
        """returns value of specified pin for current comparator (if assigned)"""
        return not bool(self.currentADC.get_cout())
 
    
