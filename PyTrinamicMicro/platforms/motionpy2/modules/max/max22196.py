################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
This file implements a basic class for using the max22196 in Command mode SPI. (CMND = HIGH && SRIAL = HIGH)
For further details refer to the data sheet.
Created on 29.04.2022
@author: TL
'''

from pyb import Pin, SPI
from PyTrinamicMicro.platforms.motionpy2.connections.spi_ic_interface import spi_ic_interface
import struct
import time

class MAX22196(object):
    '''
    This class provides basic functions to use the max22196 with command mode spi.
    For further details refer to the data sheet.
    '''

    max22196_DISTATE =0x00      # Digital Input state : DI_ is the state of the digital input pin after filtering
    max22196_FAULT1 = 0x01      # Fault1 register sources
    max22196_F1MASK = 0x02      # Mask bits controlling assertion of the \FAULT pin on the FAULT1 register events
    max22196_CNFG_x = 0x03      # IN1 Channel configuration
    max22196_GLOBLCFG = 0x0B    # Global Configuration
    max22196_LED = 0x0C         # LED or GPO On or Off Control register
    max22196_FAULT2 = 0x0D      # Fault2 register sources
    max22196_F2MASK = 0x0E      # Mask bits controlling assertion of the Fault2 bit in the Fault1 register
                                # The Fault2 bit is the logic OR of all the bits in the Fault2 register which are masked
    max22196_START_STOP = 0x0F  # Pre-Channel Start/Stop bits for counter mode
    max22196_CNT1_LSB = 0x10    # Channel 1 Counter LSB byte
    max22196_CNT1_MSB = 0x11    # Channel 1 Counter MSB byte
    max22196_CNT2_LSB = 0x12    # Channel 2 Counter LSB byte
    max22196_CNT2_MSB = 0x13    # Channel 2 Counter MSB byte
    max22196_CNT3_LSB = 0x14    # Channel 3 Counter LSB byte
    max22196_CNT3_MSB = 0x15    # Channel 3 Counter MSB byte
    max22196_CNT4_LSB = 0x16    # Channel 4 Counter LSB byte
    max22196_CNT4_MSB = 0x17    # Channel 4 Counter MSB byte
    max22196_CNT5_LSB = 0x18    # Channel 5 Counter LSB byte
    max22196_CNT5_MSB = 0x19    # Channel 5 Counter MSB byte
    max22196_CNT6_LSB = 0x1A    # Channel 6 Counter LSB byte
    max22196_CNT6_MSB = 0x1B    # Channel 6 Counter MSB byte
    max22196_CNT7_LSB = 0x1C    # Channel 7 Counter LSB byte
    max22196_CNT7_MSB = 0x1D    # Channel 7 Counter MSB byte
    max22196_CNT8_LSB = 0x1E    # Channel 8 Counter LSB byte
    max22196_CNT8_MSB = 0x1F    # Channel 8 Counter MSB byte

    def __init__(self, cs = Pin.cpu.A4, spi= 1):
        Pin(cs).value(1)
        self.__SPI = spi_ic_interface(spi=SPI(spi, SPI.MASTER, baudrate=10000, polarity=0, phase=0), cs=cs)  

    def build_byte_array(self, addr, rw, crcen, data = "00000000"):
        """returns byte array with addr, read/write, data and crc"""
        #create bytes in hex 
        TX_byte = "000"+"{:08b}".format((addr),8)[4:] + str(rw)
        crc_result_str = self.generate_CRC_encode(TX_byte, data) #calculate crc5encode

        if crcen:
            bits = TX_byte + data + crc_result_str
            send = bytearray(struct.pack("BBB", int(bits[:8],2), int(bits[8:16],2), int(bits[16:],2)))
        else:
           bits = TX_byte + data
           send = bytearray(struct.pack("BB", int(bits[:8],2), int(bits[8:],2)))
        return send 

    def bin_from_recv(self, buf, crcen):
        """returns 0/1 string equivalent from send/receive buf"""
        if crcen:
            return '{:08b}'.format(buf[0]) + '{:08b}'.format(buf[1]) + '{:08b}'.format(buf[2]) 
        else:
            return '{:08b}'.format(buf[0]) + '{:08b}'.format(buf[1]) 

    def read(self, addr, crcen):
        """sending read request and returns 24 bits 0/1 string"""
        buf_send = self.build_byte_array(addr,0,crcen)
        if crcen == 1:
            buf_recv = bytearray(3)
        else:
            buf_recv = bytearray(2)

        self.__SPI.send_recv(buf_send,buf_recv)
        read_return = self.bin_from_recv(buf_recv, crcen)

        #verify CRC
        if crcen == 1:
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
        else:
            return read_return

    def write(self, addr, crcen, data = "00000000"):
        """writing data provided as 0/1 string to addr. returns full received as string"""
        buf = self.build_byte_array(addr, 1, crcen, data)
        self.__SPI.send_recv(buf,buf)
        read_return = self.bin_from_recv(buf, crcen)

        #verify CRC
        if crcen == 1:
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
        else:
            return read_return   

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



class MAX22196PMB(object):
    """max22196 Pmod Board Class"""
    """This class provides basic functionality of max22196PMB. For further information, please see the datasheet.
    https://datasheets.maximintegrated.com/en/ds/max22196.pdf"""
    
    #max22196PMB Channels
    max22196PMB_CHANNELS = (1,2,3,4,5,6,7,8)
    max22196PMB_mode = ["1/3", "2", "HTL", "TTL"]

    def __init__(self, **kwargs):
        """
            Initialization for max22196 objects.
            
            Args:
            kwargs: dictionary specifying spi bus ("spi"), cs pin ("pin_cs"), faultB pin ("pin_faultB"), readyB pin ("pin_readyB"), latchB pin ("pin_latchB"), crcen pin ("pin_crcen")
        """
        time.sleep(0.2)

        if "pin_ready" in kwargs: #configure ready pin as input
            self.__Ready = Pin(kwargs["pin_ready"], Pin.IN)
        if "pin_fault" in kwargs: #configure fault pin as input
            self.__Fault = Pin(kwargs["pin_fault"], Pin.IN)
        if "pin_latch" in kwargs: #configure latch pin as output
            self.__Latch = Pin(kwargs["pin_latch"], Pin.OUT_PP)
            self.__Latch.value(1)
        if "pin_crcen" in kwargs: #configure crc enable pin as output, default as disabled
            self.__CRCEN = Pin(kwargs["pin_crcen"], Pin.OUT)
            self.__CRCEN.value(0)

        while self.__Ready.value() == 1:
            time.sleep(0.2) #wait for IC to be ready

        if "spi" in kwargs:
            spi = kwargs["spi"]
            if "pin_cs" in kwargs:
                self.DO = MAX22196(kwargs["pin_cs"], spi)
            self.DO.read(self.DO.max22196_FAULT1, 0)

    def get_ready_pin(self):
        return self.__Ready.value()
    
    def get_fault_pin(self):
        return self.__Fault.value()

    def get_latch_pin(self):
        return self.__Latch.value()

    def get_CRCen_pin(self):
        return self.__CRCEN.value()

    def read(self, register):
        buf = self.DO.read(register, 0)
        return buf
    
    def write(self, register, command):
        buf = self.DO.write(register, 0, command)
        return buf

    def read_DI(self):
        """Returns all channel switch status as 0/1 string"""
        # Too tired need to finish this later
        if self.__CRCEN.value() == 1:
            buf = self.DO.read(self.DO.max22196_DISTATE, 1)[8:16]
        else:
            buf = self.DO.read(self.DO.max22196_DISTATE, 0)[8:16]
        return buf

    def print_DI(self):
        if self.__CRCEN.value() == 1:
            buf = self.DO.read(self.DO.max22196_DISTATE, 1)[8:16]
        else:
            buf = self.DO.read(self.DO.max22196_DISTATE, 0)[8:16]
        print("DI states : "+str(buf))
        #distates = list()
        #distates = [int(x) for x in '{:08b}'.format(buf[1])]


    def cnfg_channel(self, channel, mode, source):
        if channel not in self.max22196PMB_CHANNELS:
            print("Error: Please select a valid channel (1-8)")
            return
        if mode not in self.max22196PMB_mode:
            print("Error: Please select a valid mode TTL, HTL, 1/3, or 2")
            return
        if source not in (0, 1):
            print("Error: Please use 1 to enable source or 0 for sink")
            return

        # Store current setting so to not change the filter settings
        if self.__CRCEN.value() == 1:
            old_data = self.DO.read(self.DO.max22196_CNFG_x + channel - 1, 1)[8:16]
        else:
            old_data = self.DO.read(self.DO.max22196_CNFG_x + channel - 1, 0)[8:16]
        # Modify HITHR and CURR depending on mode
        if mode == 'HTL':
            command = self.DO.data_generator(old_data, "000", [0,2,3])
        elif mode == '1/3':            
            command = self.DO.data_generator(old_data, "101", [0,2,3])
        elif mode == '2':            
            command = self.DO.data_generator(old_data, "010", [0,2,3])
        else:# TTL
            command = self.DO.data_generator(old_data, "011", [0,2,3])

        if source == 0:
            command = self.DO.data_generator(command, '0', [1])
            if self.__CRCEN.value() == 1:
                self.DO.write(self.DO.max22196_CNFG_x + channel - 1, 1, command)
            else:
                self.DO.write(self.DO.max22196_CNFG_x + channel - 1, 0, command)
        else:
            command = self.DO.data_generator(command, '1', [1])
            if self.__CRCEN.value() == 1:
                self.DO.write(self.DO.max22196_CNFG_x + channel - 1, 1, command)
            else:
                self.DO.write(self.DO.max22196_CNFG_x + channel - 1, 0, command)
                new_data = self.DO.read(self.DO.max22196_CNFG_x + channel - 1, 0)[8:16]

    def enable_filter(self, channel):
        if channel not in self.max22196PMB_CHANNELS:
            print("Error: Please select a valid channel (1-8)")
            return
        # Store current setting so to not change the filter settings
        if self.__CRCEN.value() == 1:
            old_data = self.DO.read(self.DO.max22196_CNFG_x + channel - 1, 1)[8:16]
        else:
            old_data = self.DO.read(self.DO.max22196_CNFG_x + channel - 1, 0)[8:16]
        command = self.DO.data_generator(old_data, "1", [3])
        
        if self.__CRCEN.value() == 1:
            self.DO.write(self.DO.max22196_CNFG_x + channel - 1, 1, command)
        else:
            self.DO.write(self.DO.max22196_CNFG_x + channel - 1, 0, command)

    def disable_filter(self, channel):
        if channel not in self.max22196PMB_CHANNELS:
            print("Error: Please select a valid channel (1-8)")
            return
        # Store current setting so to not change the filter settings
        if self.__CRCEN.value() == 1:
            old_data = self.DO.read(self.DO.max22196_CNFG_x + channel - 1, 1)[8:16]
        else:
            old_data = self.DO.read(self.DO.max22196_CNFG_x + channel - 1, 0)[8:16]
        command = self.DO.data_generator(old_data, "0", [3])
        if self.__CRCEN.value() == 1:
            self.DO.write(self.DO.max22196_CNFG_x + channel - 1, 1, command)
        else:
            self.DO.write(self.DO.max22196_CNFG_x + channel - 1, 0, command)

    def cnfg_filter(self, channel, delay):
        # see datasheet to understand how the filter counter function works in the MAX22196
        # the Delay value is stored in the CNFG_ register and can be 0x00 to 0x07 rperesenting predefined values ranging from 50µs to 20ms
        if channel not in self.max22196PMB_CHANNELS:
            print("Error: Please select a valid channel (1-8)")
            return
        if delay not in (0, 1, 2, 3, 4, 5, 6, 7):
            print("Error: Please select a delay setting (0-7)")
            return
        delay_str = "000"+"{:08b}".format((delay),8)[4:]
        # Store current setting so to not change the filter settings
        if self.__CRCEN.value() == 1:
            old_data = self.DO.read(self.DO.max22196_CNFG_x + channel - 1, 1)[8:16]
        else:
            old_data = self.DO.read(self.DO.max22196_CNFG_x + channel - 1, 0)[8:16]
        command = self.DO.data_generator(old_data, delay_str, [5,6,7])
        if self.__CRCEN.value() == 1:
            self.DO.write(self.DO.max22196_CNFG_x + channel - 1, 1, command)
        else:
            self.DO.write(self.DO.max22196_CNFG_x + channel - 1, 0, command)

    def LEDmatrix(self, mode):        
        if self.__CRCEN.value() == 1:
            old_data = self.DO.read(self.DO.max22196_GLOBLCFG, 1)[8:16]
        else:
            old_data = self.DO.read(self.DO.max22196_GLOBLCFG, 0)[8:16]
            
        if mode not in ["auto", "LED", "GPO"]:
            print("set mode as 'auto', 'LED', or 'GPO'")
            return
        if mode == 'auto':
            command = self.DO.data_generator(old_data, "10", [1,0]) # !note! data is modified backwards for some reason 
            print("LED matrix set for autonomous mode, LEDs follow state of digital input channels, LED9 indicates VMOK")
        elif mode == 'LED':
            command = self.DO.data_generator(old_data, "00", [1,0])
            print("LED mode selected. LEDs can be truned on by setting the corresponding bit in regsiter LED(0x0C)")
        else:
            command = self.DO.data_generator(old_data, "1", [0])
            print("LO1-LO6 are push-pull logic outputs controlled by bits 0:5 in register LED(0x0C)")
        
        if self.__CRCEN.value() == 1:
            self.DO.write(self.DO.max22196_GLOBLCFG, 1, command)
        else:
            self.DO.write(self.DO.max22196_GLOBLCFG, 0, command)

    def EnableCRC(self): 
        """Toggle enable pin with 0 (low) or 1 (high)"""
        self.__CRCEN.value(1)
    
    def DisableCRC(self): 
        """Toggle enable pin with 0 (low) or 1 (high)"""
        self.__CRCEN.value(0)  
    
    def Latch(self, val): 
        """set Latch high or low"""
        self.__Latch.value(val)

    def read_faults(self): 
        """Returns global errors as 0/1 string"""
        if self.__CRCEN.value() == 1:
            fault1 = self.DO.read(self.DO.max22196_FAULT1, 1)[8:16]
        else:
            fault1 = self.DO.read(self.DO.max22196_FAULT1, 0)[8:16]
        print(str(fault1))
        if int(fault1[6]) == 1:
            print("The voltage at V24 source has dropped below 16V, try using an exteral supply")
        if int(fault1[5]) == 1:
            print("The voltage at V24 source is below 7V, try using an exteral supply")
        if int(fault1[4]) == 1:
            print("The die temperature is exceeding the maximum operating temperature 115°C")
        if int(fault1[3]) == 1:
            print("Thermal Shutdown threshold (150°C, typ) has been exceeded. All input channels, input sink or source currents")
            print("and LED matrix are turned off to reduce power dissipation. GPO drivers, SPI interface and internal regulator remain active")        
        if int(fault1[1]) == 1:
            print("A POR event was detected, all registers have been returned to their POR state")
        if int(fault1[0]) == 1:
            print("An SPI CRC error was detected")

        # Fault2
        if int(fault1[2]) == 1:
            if self.__CRCEN.value() == 1:
                fault2 = self.DO.read(self.DO.max22196_FAULT2, 1)[8:16]
            else:
                fault2 = self.DO.read(self.DO.max22196_FAULT2, 0)[8:16]
            
            if int(fault2[7]) == 1:
                print("A short is detected on REFDI. All input channels are disabled")
            if int(fault2[6]) == 1:
                print("Open-circuit detected on REFDI. this could indicate a thermal shutdown")
            if int(fault2[5]) == 1:
                print("System Thermal Shutdown threshold (165°C, typ) has been exceeded. All input channels, input sink or ")
                print("source currents, LED matrix, GPO drivers, SPI interface and internal regulator are turned off to reduce power dissipation")
            if int(fault2[4]) == 1:
                print("Irregular number of SPI clk cycles detected")
            if int(fault2[3]) == 1:
                print("Voltage at VA is below undervoltage threshold")
            return  [fault1, fault2]
        return fault1
    
    def read_FAULT2(self): 
        """Returns global errors as 0/1 string"""
        return self.DO.read(self.DO.max22196_FAULT2)[8:16] 

    def check_fault(self):
        """Checks FAULT signal status. Returns True if fault detected, false is not."""
        if self.__Fault.value() == 0:
            return True #fault detected, returns fault data and prints info
        else: 
            return False

    def Fault1_mask(self, bit, enable = 1):
        """Select register bit to enable or disable fault masking""" 
        if self.__CRCEN.value() == 1:
            old_data = self.DO.read(self.DO.max22196_F1MASK, 1)[8:16]
        else:
            old_data = self.DO.read(self.DO.max22196_F1MASK, 0)[8:16]
        if enable == 1:
            command = self.DO.data_generator(old_data, "1", [7-bit])
            if self.__CRCEN.value() == 1:
                self.DO.write(self.DO.max22196_F1MASK, 1, command)
            else:
                self.DO.write(self.DO.max22196_F1MASK, 0, command)
        else: 
            command = self.DO.data_generator(old_data, "0", [7-bit])
            if self.__CRCEN.value() == 1:
                self.DO.write(self.DO.max22196_F1MASK, 1, command)
            else:
                self.DO.write(self.DO.max22196_F1MASK, 0, command)

    def Fault2_mask(self, bit, enable = 1):
        """Select register bit to enable or disable fault masking""" 
        if self.__CRCEN.value() == 1:
            old_data = self.DO.read(self.DO.max22196_F2MASK, 1)[8:16]
        else:
            old_data = self.DO.read(self.DO.max22196_F2MASK, 0)[8:16]
        if enable == 1:
            command = self.DO.data_generator(old_data, "1", [7-bit])
            if self.__CRCEN.value() == 1:
                self.DO.write(self.DO.max22196_F2MASK, 1, command)
            else:
                self.DO.write(self.DO.max22196_F2MASK, 0, command)
        else: 
            command = self.DO.data_generator(old_data, "0", [7-bit])
            if self.__CRCEN.value() == 1:
                self.DO.write(self.DO.max22196_F2MASK, 1, command)
            else:
                self.DO.write(self.DO.max22196_F2MASK, 0, command)

    def Counter_mode(self, channel, start_value):
        """
            Initialization for per channel counter mode. 
            
            Args:
            self: 
            channel: a integer value ranging from 1 to 8
            start_value: an positive integer value ranging from 0 to 2^16

            When this function is called it
            1: sets the channel's corresponding bit in the START_STOP register to 0. 
            2: writes the start_value into two 8-bit register CNTx_MSB and CNTx_LSB 
            3: ensures the LSB in F1MASK must also be set to 1.
            4: sets the channel's corresponding bit in the START_STOP register to 1. 
        """
    def exitCounter_mode(self, channel):
        """
            Exit for per channel counter mode. 
            
            Args:
            self: 
            channel: a integer value ranging from 1 to 8

            When this function is called it
            1: read DISTATE register 
            2: sets the channel's corresponding bit in the START_STOP register to 0. 
            3: writes 0x00 into two 8-bit register CNTx_MSB and CNTx_LSB  
        """
    def read_Count(self, channel):
        """
            readback for per channel counter mode. 
            
            Args:
            self: 
            channel: a integer value ranging from 1 to 8

            When this function is called it
            1: sets the channel's corresponding bit in the START_STOP register to 0. 
            2: read the two 8-bit registers CNTx_MSB and CNTx_LSB
            3: sets the channel's corresponding bit in the START_STOP register to 1, to resume counter. 

            Return:
            result: integer representing the counter value
            Fault
        """
    
