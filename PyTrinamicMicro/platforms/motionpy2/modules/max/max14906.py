'''
This file implements a basic class for the MAX14906 IC as well as 
a basic implementaion to use the module MAX14906PMB#.

Created on 28.09.2021

@author: KA
'''

from pyb import Pin, SPI
from PyTrinamicMicro.platforms.motionpy2.connections.spi_ic_interface import spi_ic_interface
import time
import struct

class  MAX14906(object):
    '''This class provides basic functions to use the MAX14906, for further details refer to the data sheet.'''
    MAX14906_SETOUT_adr=0x00      #Set mode R&W 
    MAX14906_SETLED_adr=0x01      #Status/Fault LED R&W 
    MAX14906_DOILEVEL_adr=0x02    #Driver Output level R&C
    MAX14906_INTERRUPT_adr=0x03   #Interrupt R
    MAX14906_OVRLDCHF_adr=0x04    #Current Limit Fault R&C
    MAX14906_OPNWIRCHF_adr=0x05   #Voltage Limit Fault R&C 
    MAX14906_SHTVDDCHF_adr=0x06   #Short to VDD Fault R&C 
    MAX14906_GLOBALERR_adr=0x07   #Global Error Fault R&C 
    MAX14906_OPNWREN_adr=0x08     #Open Wire Enable R&W
    MAX14906_SHTVDDEN_adr=0x09    #Short to VDD Enable R&W 
    MAX14906_CONFIG1_adr=0x0a     #Configure 1 R&W 
    MAX14906_CONFIG2_adr=0x0b     #Configure 2 R&W
    MAX14906_CONFIGDI_adr=0x0c    #Configure Driver Input R&W 
    MAX14906_CONFIGDO_adr=0x0d    #Configure Driver Output R&W 
    MAX14906_CURRLIM_adr=0x0e     #Set Current Limit R&W 
    MAX14906_MASK_adr=0x0f        #Mask R&W 
    MAX14906_CHANNEL = {1, 2, 3, 4}
    MAX14906_CURRLIM = {"600mA", "130mA", "300mA", "1.2A"}

    def __init__(self, cs = Pin.cpu.A4, spi= 1):
        Pin(cs).value(1)
        self.__SPI = spi_ic_interface(spi=SPI(spi, SPI.MASTER, baudrate=10000, polarity=0, phase=0), cs=cs)  

    def build_byte_array(self, addr, rw, data = "00000000"):
        """returns byte array with addr, read/write, data and crc"""
        #create bytes in hex 
        TX_byte = "000"+"{:08b}".format((addr),8)[4:] + str(rw)
        crc_result_str = self.generate_CRC_encode(TX_byte, data) #calculate crc5encode

        bits = TX_byte + data + crc_result_str
        send = bytearray(struct.pack("BBB", int(bits[:8],2), int(bits[8:16],2), int(bits[16:],2)))
        return send 

    def bin_from_recv(self, buf):
        """returns 0/1 string equivalent from send/receive buf"""
        return '{:08b}'.format(buf[0]) + '{:08b}'.format(buf[1]) + '{:08b}'.format(buf[2]) 

    def read(self, addr):
        """sending read request and returns 24 bits 0/1 string"""
        buf_send = self.build_byte_array(addr,0)
        buf_recv = bytearray(3)
        self.__SPI.send_recv(buf_send,buf_recv)
        read_return = self.bin_from_recv(buf_recv)

        #verify CRC
        byte1 = read_return[:8]
        byte2 = read_return[8:16]
        byte3 = read_return[16:]
        calculated_crc = self.generate_CRC_decode(byte1, byte2, byte3) #calculate CRC value from returned buf
        if calculated_crc[3:] == read_return[19:]: #checks only calculated CRC with returned CRC 
            return read_return
        else:
		    print("Read Function")
            print("Return Buffer: ", read_return)
            print("Calculated CRC: ", calculated_crc[3:])
            print("Received CRC: ", read_return[19:])
            print("Err: CHECK CRC ")
            return read_return

    def write(self, addr, data = "00000000"):
        """writing data provided as 0/1 string to addr. returns full received as string"""
        buf = self.build_byte_array(addr, 1, data)
        self.__SPI.send_recv(buf,buf)
        read_return = self.bin_from_recv(buf)

        #verify CRC
        byte1 = read_return[:8]
        byte2 = read_return[8:16]
        byte3 = read_return[16:]
        calculated_crc = self.generate_CRC_decode(byte1, byte2, byte3) #calculate new CRC value from returned buf
        if calculated_crc[3:] == read_return[19:]: #checks only calculated with returned CRC 
            return read_return
        else:
            print("Write Function")
            print("Return buf: ", read_return)
            print("Calculated CRC: ", calculated_crc[3:])
            print("Received CRC: ", read_return[19:])
            print("Err: CHECK CRC ")
            
    def generate_CRC_encode(self, TX_byte, data_byte):
        """Calculates crc5 encode"""
        TX_byte_int = int(TX_byte, 2)
        data_byte_int = int(data_byte, 2)

        crc5_start = 31 #0x1f
        crc5_poly = 21 #0x15
        crc_result = crc5_start 
        
        #TX_byte
        for i in range(0, 8):
            if (((TX_byte_int >> (7-i)) & 1) ^ ((crc_result & 16) >> 4)) > 0 : 
                crc_result = (crc5_poly ^ ((crc_result << 1) & 31))
            else: 
                crc_result = ((crc_result << 1) & 31) #shift left and keep lower 6 bits

        #data_byte 
        for i in range(0, 8):
            if (((data_byte_int >> (7-i)) & 1) ^ ((crc_result & 16) >> 4)) > 0 : 
                crc_result = (crc5_poly ^ ((crc_result << 1) & 31))
            else: 
                crc_result = ((crc_result << 1) & 31) #shift left and keep lower 6 bits
        
        #set three extra bits to zero 
        byte3 = 0
        for i in range(0, 3):
            if (((byte3 >> (7-i)) & 1) ^ ((crc_result & 16) >> 4)) > 0 : 
                crc_result = (crc5_poly ^ ((crc_result << 1) & 31))
            else: 
                crc_result = ((crc_result << 1) & 31) #shift left and keep lower 6 bits
            
        crc_result_str = str(bin(crc_result))[2:]
        while len(crc_result_str) < 8: #zero pad
            crc_result_str = "0" + crc_result_str 
        return crc_result_str

    def generate_CRC_decode(self, byte1, byte2, byte3):
        """Calculates crc5 decode"""
        byte1_int = int(byte1, 2)
        byte2_int = int(byte2, 2)
        byte3_int = int(byte3, 2)

        #calculate crc5decode
        crc5_start = 31 #0x1f
        crc5_poly = 21 #0x15
        crc_result = crc5_start 
        
        #Byte 1
        for i in range(2, 8):
            if (((byte1_int >> (7-i)) & 1)^((crc_result & 16) >> 4)) > 0 : 
                crc_result = (crc5_poly ^ ((crc_result << 1) & 31))
            else: 
                crc_result = ((crc_result << 1) & 31) #shift left and keep lower 6 bits

        #data_byte 
        for i in range(0, 8):
            if (((byte2_int >> (7-i)) & 1) ^ ((crc_result & 16) >> 4)) > 0 : 
                crc_result = (crc5_poly ^ ((crc_result << 1) & 31))
            else: 
                crc_result = ((crc_result << 1) & 31) #shift left and keep lower 6 bits

        for i in range(0, 3):
            if (((byte3_int >> (7-i)) & 1) ^ ((crc_result & 16) >> 4)) > 0 : 
                crc_result = (crc5_poly ^ ((crc_result << 1) & 31))
            else: 
                crc_result = ((crc_result << 1) & 31) #shift left and keep lower 6 bits
            
        crc_result_str = str(bin(crc_result))[2:]
        while len(crc_result_str) < 8: #zero pad
            crc_result_str = "0" + crc_result_str 
        return crc_result_str
        
    def data_generator(self, old_data, new_data, location):
        """Changes specified bits in old_data with new_data"""
        list_data = list(old_data)
        for i in range(0, len(location)):
            list_data[location[i]] = new_data[i]
        old_data = "".join(list_data)
        return old_data

class  MAX14906PMB(object):
    '''This class provides basic functions to use the MAX14906PMB#, for further details refer to the data sheet.'''
    spi = 1
    def __init__(self, **kwargs):
        time.sleep(0.2)
        if "pin_ready" in kwargs: #configure ready pin as input
            self.__Ready = Pin(kwargs["pin_ready"], Pin.IN)
        if  "pin_fault" in kwargs: #configure fault pin as input
            self.__Fault = Pin(kwargs["pin_fault"], Pin.IN) 
        if  "pin_synch" in kwargs: #configure synch pin as output
            self.__Synch = Pin(kwargs["pin_synch"], Pin.OUT)
            self.__Synch.value(1)
        if  "pin_enable" in kwargs: #configure enable pin as output
            self.__Enable = Pin(kwargs["pin_enable"], Pin.OUT)
            self.__Enable.value(1)  
        while self.__Ready.value() == 1:
            time.sleep(0.1)
            print("Not Ready.")
        if "spi" in kwargs:
            spi = kwargs["spi"]   
            if  "pin_cs" in kwargs: 
                self.DO = MAX14906(kwargs["pin_cs"], spi) #initialize object
                self.DO.read(self.DO.MAX14906_GLOBALERR_adr)
                self.DO.write(self.DO.MAX14906_CONFIGDI_adr, "00001000") #configure DoiLevels 00001000

                self.enable_GDrv(1) #enable gate drivers for external PMOS
                self.enable_GDrv(2)
                self.enable_GDrv(3)
                self.enable_GDrv(4) 

    def high_z_mode(self, channel):
        """Sets specified channel to high impedance, low leakage mode"""
        if channel not in self.DO.MAX14906_CHANNEL:
            print("ERROR: Please select valid channel") 
            return 
        else: 
            self.set_DI(channel)
            old_data = self.DO.read(self.DO.MAX14906_CONFIGDO_adr)[8:16]
            if old_data[8-(2*channel)] == "0":
                command = self.DO.data_generator(old_data, "1", [8-(2*channel)])
                self.DO.write(self.DO.MAX14906_CONFIGDO_adr, command)

    def static_low_mode(self, channel):
        """Sets desired channel static low mode"""
        if channel not in self.DO.MAX14906_CHANNEL:
            print("ERROR: Please select valid channel") 
            return 
        else:
            self.set_DO(channel)
            return "0"
        
    def static_high_mode(self, channel): 
        """Sets desired channel static high mode"""
        if channel not in self.DO.MAX14906_CHANNEL:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14906_SETOUT_adr)[8:16]
            command = self.DO.data_generator(old_data, "1", [8-channel])
            self.DO.write(self.DO.MAX14906_SETOUT_adr, command)
            return "1"
        
    def set_DI(self, channel): 
        """Sets specified channel to digital input mode"""
        if channel not in self.DO.MAX14906_CHANNEL:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14906_SETOUT_adr)[8:16]
            if old_data[4-channel] == "0": #check if bit low
                command = self.DO.data_generator(old_data, "1", [4-channel])
                self.DO.write(self.DO.MAX14906_SETOUT_adr, command)
            old_data = self.DO.read(self.DO.MAX14906_CONFIGDO_adr)[8:16] #set DO mode bits to 0X
            if old_data[8-(2*channel)] == "1": 
                command = self.DO.data_generator(old_data, "0", [8-(2*channel)])
                self.DO.write(self.DO.MAX14906_CONFIGDO_adr, command)
                
    def high_side_mode(self, channel): 
        """Sets specified channel to high-side mode"""
        if channel not in self.DO.MAX14906_CHANNEL:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14906_CONFIGDO_adr)[8:16]
            if old_data[8-(2*channel)] == "1" or old_data[8-((2*channel)-1)] == "1": 
                command = self.DO.data_generator(old_data, "00", [8-(2*channel), 8-((2*channel) -1)])
                self.DO.write(self.DO.MAX14906_CONFIGDO_adr, command)

    def high_side_modex2(self, channel): 
        """Set specified channel to high-side_mode x2 inrush current"""
        if channel not in self.DO.MAX14906_CHANNEL:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14906_CONFIGDO_adr)[8:16]
            if old_data[8-(2*channel)] == "1" or old_data[8-((2*channel) -1)] == "0": 
                command = self.DO.data_generator(old_data, "01", [8-(2*channel), 8-((2*channel) -1)])
                self.DO.write(self.DO.MAX14906_CONFIGDO_adr, command)
    
    def push_pull_mode_active(self, channel): 
        """Sets specified channel to push-pull mode active"""
        if channel not in self.DO.MAX14906_CHANNEL:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14906_CONFIGDO_adr)[8:16]
            if old_data[8-(2*channel)] == "0" or old_data[8-((2*channel) -1)] == "1": 
                command = self.DO.data_generator(old_data, "10", [8-(2*channel), 8-((2*channel) -1)])
                self.DO.write(self.DO.MAX14906_CONFIGDO_adr, command)
            
    def push_pull_mode_simple(self, channel): 
        """Sets specified channel to push pull mode simple"""
        if channel not in self.DO.MAX14906_CHANNEL:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14906_CONFIGDO_adr)[8:16]
            if old_data[8-(2*channel)] == "0" or old_data[8-((2*channel) -1)] == "0": 
                command = self.DO.data_generator(old_data, "11", [8-(2*channel), 8-((2*channel) -1)])
                self.DO.write(self.DO.MAX14906_CONFIGDO_adr, command)            
           
    def current_lim_set(self, channel, setCurr):
        """Sets specified channel to have specified current limiting"""
        """600mA, 130mA, 300mA, 1.2A """
        if channel not in self.DO.MAX14906_CHANNEL:
            print("ERROR: Please select valid channel") 
            return 
        elif setCurr not in self.DO.MAX14906_CURRLIM:
            print("ERROR: Please select from 600mA, 130mA, 300mA, or 1.2A")
        else:
            old_data = self.DO.read(self.DO.MAX14906_CURRLIM_adr)[8:16]
            if setCurr == "600mA": 
                if old_data[8-(2*channel)] == "1" or old_data[8-((2*channel) -1)] == "1": 
                    command = self.DO.data_generator(old_data, "00", [8-(2*channel), 8-((2*channel) -1)])
                    self.DO.write(self.DO.MAX14906_CURRLIM_adr, command)
            if setCurr == "130mA": 
                if old_data[8-(2*channel)] == "1" or old_data[8-((2*channel) -1)] == "0": 
                    command = self.DO.data_generator(old_data, "01", [8-(2*channel), 8-((2*channel) -1)])
                    self.DO.write(self.DO.MAX14906_CURRLIM_adr, command)   
            if setCurr == "300mA": 
                if old_data[8-(2*channel)] == "0" or old_data[8-((2*channel) -1)] == "1": 
                    command = self.DO.data_generator(old_data, "10", [8-(2*channel), 8-((2*channel) -1)])
                    self.DO.write(self.DO.MAX14906_CURRLIM_adr, command) 
            if setCurr == "1.2A": 
                if old_data[8-(2*channel)] == "0" or old_data[8-((2*channel) -1)] == "0": 
                    command = self.DO.data_generator(old_data, "11", [8-(2*channel), 8-((2*channel) -1)])
                    self.DO.write(self.DO.MAX14906_CURRLIM_adr, command)   
    
    def DI_type(self, type): 
        """Changes ALL digital input channel types to Type 1, 2, or 3"""
        if type not in {1, 2, 3}:
                print("ERROR: Please select valid type") 
                return 
        else:
            old_data = self.DO.read(self.DO.MAX14906_CONFIGDI_adr)[8:16]
            if old_data[0] == "1" and (type == 1 or type == 3): 
                command = self.DO.data_generator(old_data, "0", [0])
                self.DO.write(self.DO.MAX14906_CONFIGDI_adr, command) 
            if old_data[0] == "0" and type == 2:
                command = self.DO.data_generator(old_data, "1", [0])
                self.DO.write(self.DO.MAX14906_CONFIGDI_adr, command)

    def read_DI(self, channel):
        """Returns logic level of specified channel if in DI mode as 0/1 string"""
        if channel not in self.DO.MAX14906_CHANNEL:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14906_CONFIGDI_adr)[8:16]
            clear_VDDFaultsel = self.DO.data_generator(old_data, "0", [3])
            self.DO.write(self.DO.MAX14906_CONFIGDI_adr, clear_VDDFaultsel) #clear VDDFaultsel first
            data = self.DO.read(self.DO.MAX14906_DOILEVEL_adr)[8:16]
            return data[8-channel]

    def set_DO(self, channel): 
        """Sets specified channel to digital output mode"""
        if channel not in self.DO.MAX14906_CHANNEL:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14906_SETOUT_adr)[8:16]
            if old_data[4-channel] == "1" or old_data[8-channel] == "1": #check if bit enabled DI
                command = self.DO.data_generator(old_data, "00", [4-channel, 8-channel]) #set both configure and output pin low
                self.DO.write(self.DO.MAX14906_SETOUT_adr, command)

    def SLED_control(self, enable = 1):
        """Enables manual control to LEDs if enable = 1, if enable = 0 disables manual control"""
        old_data = self.DO.read(self.DO.MAX14906_CONFIG1_adr)[8:16]
        if enable == 1 and old_data[6] == "0":
            command = self.DO.data_generator(old_data, "1", [6])
            self.DO.write(self.DO.MAX14906_CONFIG1_adr, command) 
        if enable == 0 and old_data[6] == "1":
            command = self.DO.data_generator(old_data, "0", [6])
            self.DO.write(self.DO.MAX14906_CONFIG1_adr, command) 

    def set_SLED(self, LED, val):
        """Turns LEDs on if val = 1 or off if val = 0"""
        if LED not in self.DO.MAX14906_CHANNEL:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14906_SETLED_adr)[8:16]
            if val == 1 and old_data[4-LED] == "0": 
                command = self.DO.data_generator(old_data, "1", [4-LED])
                self.DO.write(self.DO.MAX14906_SETLED_adr, command)
            if val == 0 and old_data[4-LED] == '1':
                command = self.DO.data_generator(old_data, "0", [4-LED])
                self.DO.write(self.DO.MAX14906_SETLED_adr, command)
		
    def FLED_control(self, enable = 1):
        """Enables manual control to FLEDs if enable = 1, if enable = 0 disables manual control"""
        old_data = self.DO.read(self.DO.MAX14906_CONFIG1_adr)[8:16]
        if enable == 1 and old_data[7] == "0":
            command = self.DO.data_generator(old_data, "1", [7])
            self.DO.write(self.DO.MAX14906_CONFIG1_adr, command) 
        if enable == 0 and old_data[7] == "1":
            command = self.DO.data_generator(old_data, "0", [7])
            self.DO.write(self.DO.MAX14906_CONFIG1_adr, command) 

    def set_FLED(self, FLED, val): 
        """Turns FLEDs on if val = 1 or off if val = 0"""
        if FLED not in self.DO.MAX14906_CHANNEL:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14906_SETLED_adr)[8:16]
            if val == 1 and old_data[8-FLED] == "0": 
                command = self.DO.data_generator(old_data, "1", [8-FLED])
                self.DO.write(self.DO.MAX14906_SETLED_adr, command)
            if val == 0 and old_data[8-FLED] == '1':
                command = self.DO.data_generator(old_data, "0", [8-FLED])
                self.DO.write(self.DO.MAX14906_SETLED_adr, command)
		
    def EN(self, val): 
        """Toggle enable pin with 0 (low) or 1 (high)"""
        self.__Enable.value(val)  
    
    def SYNCH(self, val): 
        """Toggle enable pin with 0 (low) or 1 (high)"""
        self.__Synch.value(val)

    def read_global_err(self): 
        """Returns global errors as 0/1 string"""
        return self.DO.read(self.DO.MAX14906_GLOBALERR_adr)[8:16]       

    def check_fault(self):
        """Checks FAULT signal status. Returns True if fault detected, false is not."""
        if self.__Fault.value() == 0:
            return True #fault detected
        else: 
            return False
        
    def enable_OW_fault(self, channel):
        """Enables OW fault for specified channel"""
        if channel not in self.DO.MAX14906_CHANNEL:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14906_OPNWREN_adr)[8:16]
            if old_data[8-channel] == "0": 
                command = self.DO.data_generator(old_data, "1", [8-channel])
                self.DO.write(self.DO.MAX14906_OPNWREN_adr, command)
    
    def disable_OW_fault(self, channel):
        """Disables OW fault for specified channel"""
        if channel not in self.DO.MAX14906_CHANNEL:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14906_OPNWREN_adr)[8:16]
            if old_data[8-channel] == "1": 
                command = self.DO.data_generator(old_data, "0", [8-channel])
                self.DO.write(self.DO.MAX14906_OPNWREN_adr, command)

    def enable_fault_latching(self, latching = 1):
        """Enables (latching = 1) or disables (latching = 0) diagnostic fault bits"""
        old_data = self.DO.read(self.DO.MAX14906_CONFIG1_adr)[8:16]
        if latching == 1 and old_data[1] == "0":
            command = self.DO.data_generator(old_data, "1", [1])
            self.DO.write(self.DO.MAX14906_CONFIG1_adr, command) 
        if latching == 0 and old_data[1] == "1":
            command = self.DO.data_generator(old_data, "0", [1])
            self.DO.write(self.DO.MAX14906_CONFIG1_adr, command) 

    def read_OW_fault(self):
        """Returns all four channel OW faults as 0/1 string"""
        return self.DO.read(self.DO.MAX14906_OPNWIRCHF_adr)[12:16]

    def enable_ShVDD(self, channel):
        """Enables short to VDD detection on specified channel"""
        if channel not in self.DO.MAX14906_CHANNEL:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14906_SHTVDDEN_adr)[8:16]
            if old_data[8-channel] == "0": 
                command = self.DO.data_generator(old_data, "1", [8-channel])
                self.DO.write(self.DO.MAX14906_SHTVDDEN_adr, command)
    
    def disable_ShVDD(self, channel):
        """Disables short to VDD detection on specified channel"""
        if channel not in self.DO.MAX14906_CHANNEL:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14906_SHTVDDEN_adr)[8:16]
            if old_data[8-channel] == "1": 
                command = self.DO.data_generator(old_data, "0", [8-channel])
                self.DO.write(self.DO.MAX14906_SHTVDDEN_adr, command)

    def read_ShVDD_fault(self): 
        """Returns all four channel Short to VDD fault as 0/1 string"""
        return self.DO.read(self.DO.MAX14906_SHTVDDCHF_adr)[12:16]

    def enable_GDrv(self, channel): 
        """Enables gate driver for external PMOS transistor on specified channel"""     
        if channel not in self.DO.MAX14906_CHANNEL:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14906_OPNWREN_adr)[8:16]
            if old_data[4-channel] == "0": 
                command = self.DO.data_generator(old_data, "1", [4-channel])
                self.DO.write(self.DO.MAX14906_OPNWREN_adr, command)
    
    def disable_GDrv(self, channel): 
        """Disables gate driver for external PMOS transistor on specified channel"""     
        if channel not in self.DO.MAX14906_CHANNEL:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14906_OPNWREN_adr)[8:16]
            if old_data[4-channel] == "1": 
                command = self.DO.data_generator(old_data, "0", [4-channel])
                self.DO.write(self.DO.MAX14906_OPNWREN_adr, command)
    
    def read_Interrupt(self):
        return self.DO.read(self.DO.MAX14906_INTERRUPT_adr)

    def masking(self, bit, enable = 1):
        """Select register bit to enable or disable fault masking""" 
        
        old_data = self.DO.read(self.DO.MAX14906_MASK_adr)[8:16]
        if enable == 1:
            command = self.DO.data_generator(old_data, "1", [7-bit])
            self.DO.write(self.DO.MAX14906_MASK_adr, command)
        else: 
            command = self.DO.data_generator(old_data, "0", [7-bit])
            self.DO.write(self.DO.MAX14906_MASK_adr, command)