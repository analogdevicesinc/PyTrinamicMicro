'''
This file implements a basic class for using the MAX14916 in Command mode SPI. (CMND = HIGH && SRIAL = HIGH)
For further details refer to the data sheet.
Created on 29.04.2022
@author: TL
'''

from pyb import Pin, SPI
from PyTrinamicMicro.platforms.motionpy2.connections.spi_ic_interface import spi_ic_interface
import struct
import time

class MAX14916(object):
    '''
    This class provides basic functions to use the MAX14916 with command mode spi.
    For further details refer to the data sheet.
    '''

    MAX14916_SET_OUT_REG =0x00 #Set Output Register Address
    MAX14916_SET_FLED_REG = 0x01 #Fault LED Register Address
    MAX14916_SET_SLED_REG = 0x02 #Status LED Register Address
    MAX14916_INTERRUPT_REG = 0x03 #Interrupt Status Register Address
    MAX14916_OVL_CHF_REG = 0x04 #Overload fault Register Address
    MAX14916_CURRENT_LIM_REG = 0x05 #Current Limit fault Register Address
    MAX14916_OW_OFF_CHF_REG = 0x06 #Open-Wire Detect (Channel OFF) fault Register Address
    MAX14916_OW_ON_CHF_REG = 0x07 #Open-Wire Detect (Channel ON) fault Register Address
    MAX14916_SHRT_VDD_CHF_REG = 0x08 #Short-Vdd fault Register Address
    MAX14916_GLBL_ERR_REG = 0x09 #Global Fault Register Address
    MAX14916_OW_OFF_EN_REG = 0x0A #Open-Wire Detect (Channel OFF) enable Register Address
    MAX14916_OW_ON_EN_REG = 0x0B #Open-Wire Detect (Channel ON) enable Register Address
    MAX14916_SHRT_VDD_EN_REG = 0x0C #Short-Vdd enable Register Address
    MAX14916_CONFIG1_REG = 0x0D #Configuration 1 Register Address
    MAX14916_CONFIG2_REG = 0x0E #Configuration 2 Register Address
    MAX14916_MASK_REG = 0x0F #Interrupt Mask Register Address

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



class MAX14916PMB(object):
    """MAX14916 Pmod Board Class"""
    """This class provides basic functionality of MAX14916PMB. For further information, please see the datasheet.
    https://datasheets.maximintegrated.com/en/ds/MAX14916.pdf"""
    
    #MAX14916PMB Channels
    MAX14916PMB_CHANNELS = (1,2,3,4)

    def __init__(self, **kwargs):
        """
            Initialization for 14916 objects.
            
            Args:
            kwargs: dictionary specifying spi bus ("spi"), cs pin ("pin_cs"), and intb pin ("pin_intb")
        """
        time.sleep(0.2)

        if "pin_ready" in kwargs: #configure ready pin as input
            self.__Ready = Pin(kwargs["pin_ready"], Pin.IN)
        if "pin_fault" in kwargs: #configure fault pin as input
            self.__Fault = Pin(kwargs["pin_fault"], Pin.IN)
        if "pin_synch" in kwargs: #configure synch pin as output
            self.__Synch = Pin(kwargs["pin_synch"], Pin.OUT)
            self.__Synch.value(1)
        if "pin_enable" in kwargs: #configure enable pin as output
            self.__Enable = Pin(kwargs["pin_enable"], Pin.OUT)
            self.__Enable.value(1)

        while self.__Ready.value() == 1:
            time.sleep(0.2) #wait for IC to be ready

        if "spi" in kwargs:
            spi = kwargs["spi"]
            if "pin_cs" in kwargs:
                self.DO = MAX14916(kwargs["pin_cs"], spi)
                self.DO.read(self.DO.MAX14916_GLBL_ERR_REG) #Clear the initial intterupt flag

    def set_HSS(self, channel):
        """Turn ON high-side switch channel"""
        if channel not in self.MAX14916PMB_CHANNELS:
            print("Error: Please select a valid channel (1-4)")
            return
            
        old_data = self.DO.read(self.DO.MAX14916_SET_OUT_REG)[8:16]
        if old_data[7-(channel-1)*2] == "0":
            command = self.DO.data_generator(old_data, "11", [7-(channel-1)*2,6-(channel-1)*2])
            self.DO.write(self.DO.MAX14916_SET_OUT_REG, command) 

    def clear_HSS(self, channel):
        """Turn OFF high-side switch channel"""
        if channel not in self.MAX14916PMB_CHANNELS:
            print("Error: Please select a valid channel (1-4)")
            return
            
        old_data = self.DO.read(self.DO.MAX14916_SET_OUT_REG)[8:16]
        if old_data[7-(channel-1)*2] == "1":
            command = self.DO.data_generator(old_data, "00", [7-(channel-1)*2,6-(channel-1)*2])
            self.DO.write(self.DO.MAX14916_SET_OUT_REG, command) 

    def read_HSS(self):
        """Returns all channel switch status as 0/1 string"""
        return self.DO.read(self.DO.MAX14916_SET_OUT_REG)[8:16]

    def SLED_control(self, enable):
        """Set control configuration for status LED control"""
        old_data = self.DO.read(self.DO.MAX14916_CONFIG1_REG)[8:16]
        if enable == 1 and old_data[6] == "0":
            command = self.DO.data_generator(old_data, "1", [6])
            self.DO.write(self.DO.MAX14916_CONFIG1_REG, command) 
        if enable == 0 and old_data[6] == "1":
            command = self.DO.data_generator(old_data, "0", [6])
            self.DO.write(self.DO.MAX14916_CONFIG1_REG, command) 


    def set_SLED(self, SLED, val):
        """Turns LEDs on if val = 1 or off if val = 0"""
        if SLED not in self.MAX14916PMB_CHANNELS:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14916_SET_SLED_REG)[8:16]
            if val == 1 and old_data[7-(SLED-1)*2] == "0": 
                command = self.DO.data_generator(old_data, "11", [7-(SLED-1)*2,6-(SLED-1)*2])
                self.DO.write(self.DO.MAX14916_SET_SLED_REG, command)
            if val == 0 and old_data[7-(SLED-1)*2] == '1':
                command = self.DO.data_generator(old_data, "00", [7-(SLED-1)*2,6-(SLED-1)*2])
                self.DO.write(self.DO.MAX14916_SET_SLED_REG, command)

    def FLED_control(self, enable):
        """Enables manual control to FLEDs if enable = 1, if enable = 0 disables manual control"""
        old_data = self.DO.read(self.DO.MAX14916_CONFIG1_REG)[8:16]
        if enable == 1 and old_data[7] == "0":
            command = self.DO.data_generator(old_data, "1", [7])
            self.DO.write(self.DO.MAX14916_CONFIG1_REG, command) 
        if enable == 0 and old_data[7] == "1":
            command = self.DO.data_generator(old_data, "0", [7])
            self.DO.write(self.DO.MAX14916_CONFIG1_REG, command)
    
    def set_FLED(self, FLED, val):
        """Turns FLEDs on if val = 1 or off if val = 0"""
        if FLED not in self.MAX14916PMB_CHANNELS:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14916_SET_FLED_REG)[8:16]
            if val == 1 and old_data[7-(FLED-1)*2] == "0": 
                command = self.DO.data_generator(old_data, "11", [7-(FLED-1)*2,6-(FLED-1)*2])
                self.DO.write(self.DO.MAX14916_SET_FLED_REG, command)
            if val == 0 and old_data[7-(FLED-1)*2] == '1':
                command = self.DO.data_generator(old_data, "00", [7-(FLED-1)*2,6-(FLED-1)*2])
                self.DO.write(self.DO.MAX14916_SET_FLED_REG, command) 

    def EN(self, val): 
        """Toggle enable pin with 0 (low) or 1 (high)"""
        self.__Enable.value(val)  
    
    def SYNCH(self, val): 
        """Toggle enable pin with 0 (low) or 1 (high)"""
        self.__Synch.value(val)

    def read_global_err(self): 
        """Returns global errors as 0/1 string"""
        return self.DO.read(self.DO.MAX14916_GLBL_ERR_REG)[8:16]       

    def check_fault(self):
        """Checks FAULT signal status. Returns True if fault detected, false is not."""
        if self.__Fault.value() == 0:
            return True #fault detected
        else: 
            return False
    
    def enable_OW_ON_fault(self, channel):
        """Enables OW fault for specified channel"""
        if channel not in self.MAX14916PMB_CHANNELS:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14916_OW_ON_EN_REG)[8:16]
            if old_data[7-(channel-1)*2] == "0": 
                command = self.DO.data_generator(old_data, "11", [7-(channel-1)*2,6-(channel-1)*2])
                self.DO.write(self.DO.MAX14916_OW_ON_EN_REG, command)
    
    def disable_OW_ON_fault(self, channel):
        """Disables OW fault for specified channel"""
        if channel not in self.MAX14916PMB_CHANNELS:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14916_OW_ON_EN_REG)[8:16]
            if old_data[7-(channel-1)*2] == "1": 
                command = self.DO.data_generator(old_data, "00", [7-(channel-1)*2,6-(channel-1)*2])
                self.DO.write(self.DO.MAX14916_OW_ON_EN_REG, command)

    def read_OW_ON_fault(self):
        """Returns all open-wire ON faults as 0/1 string"""
        return self.DO.read(self.DO.MAX14916_OW_ON_CHF_REG)[8:16]

    def enable_OW_OFF_fault(self, channel):
        """Enables OW fault for specified channel"""
        if channel not in self.MAX14916PMB_CHANNELS:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14916_OW_OFF_EN_REG)[8:16]
            if old_data[7-(channel-1)*2] == "0": 
                command = self.DO.data_generator(old_data, "11", [7-(channel-1)*2,6-(channel-1)*2])
                self.DO.write(self.DO.MAX14916_OW_OFF_EN_REG, command)
    
    def disable_OW_OFF_fault(self, channel):
        """Disables OW fault for specified channel"""
        if channel not in self.MAX14916PMB_CHANNELS:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14916_OW_OFF_EN_REG)[8:16]
            if old_data[7-(channel-1)*2] == "1": 
                command = self.DO.data_generator(old_data, "00", [7-(channel-1)*2,6-(channel-1)*2])
                self.DO.write(self.DO.MAX14916_OW_OFF_EN_REG, command)

    def read_OW_OFF_fault(self):
        return self.DO.read(self.DO.MAX14916_OW_OFF_CHF_REG)[8:16]

    def enable_ShVDD(self, channel):
        """Enables short to VDD detection on specified channel"""
        if channel not in self.MAX14916PMB_CHANNELS:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14916_SHRT_VDD_EN_REG)[8:16]
            if old_data[7-(channel-1)*2] == "0": 
                command = self.DO.data_generator(old_data, "11", [7-(channel-1)*2,6-(channel-1)*2])
                self.DO.write(self.DO.MAX14916_SHRT_VDD_EN_REG, command)
    
    def disable_ShVDD(self, channel):
        """Disables short to VDD detection on specified channel"""
        if channel not in self.MAX14916PMB_CHANNELS:
            print("ERROR: Please select valid channel") 
            return 
        else:
            old_data = self.DO.read(self.DO.MAX14916_SHRT_VDD_EN_REG)[8:16]
            if old_data[7-(channel-1)*2] == "1": 
                command = self.DO.data_generator(old_data, "00", [7-(channel-1)*2,6-(channel-1)*2])
                self.DO.write(self.DO.MAX14916_SHRT_VDD_EN_REG, command)

    def read_ShVDD_fault(self): 
        """Returns all four channel Short to VDD fault as 0/1 string"""
        return self.DO.read(self.DO.MAX14916_SHRT_VDD_CHF_REG)[8:16]

    def read_Interrupt(self):
        """Returns interrupt register values as 0/1 string"""
        return self.DO.read(self.DO.MAX14916_INTERRUPT_REG)

    def read_CurrLim_fault(self): 
        """Returns all channel current faults as 0/1 string"""
        return self.DO.read(self.DO.MAX14916_CURRENT_LIM_REG)[8:16]

    def set_FLED_stretch(self, timeout):
        """Set fault LED minimum on-time after fault"""
        if timeout not in ["0s","1s","2s","3s"]:
            print("SPI watchdog timeout must be 0s, 1s, 2s, or 3s")
            return

        old_data = self.DO.read(self.DO.MAX14916_CONFIG1_REG)[8:16]
        if timeout == "0s":
            command = self.DO.data_generator(old_data, "00", [5,4])
            self.DO.write(self.DO.MAX14916_CONFIG1_REG, command)
        if timeout == "1s":
            command = self.DO.data_generator(old_data, "01", [5,4])
            self.DO.write(self.DO.MAX14916_CONFIG1_REG, command)
        if timeout == "2s":
            command = self.DO.data_generator(old_data, "10", [5,4])
            self.DO.write(self.DO.MAX14916_CONFIG1_REG, command)
        if timeout == "3s":
            command = self.DO.data_generator(old_data, "11", [5,4])
            self.DO.write(self.DO.MAX14916_CONFIG1_REG, command)

    def enable_FFilter (self):
        """Enable fault signal filtering and blanking"""
        old_data = self.DO.read(self.DO.MAX14916_CONFIG1_REG)[8:16]
        if old_data[3] == "0":
            command = self.DO.data_generator(old_data, "1", [3])
            self.DO.write(self.DO.MAX14916_CONFIG1_REG, command)

    def disable_FFilter (self):
        """Real-Time fault detection without filtering or blanking"""
        old_data = self.DO.read(self.DO.MAX14916_CONFIG1_REG)[8:16]
        if old_data[3] == "1":
            command = self.DO.data_generator(old_data, "0", [3])
            self.DO.write(self.DO.MAX14916_CONFIG1_REG, command)

    def enable_FiltrLong (self):
        """Select long blanking time (8ms) for fault bits"""
        old_data = self.DO.read(self.DO.MAX14916_CONFIG1_REG)[8:16]
        if old_data[2] == "0":
            command = self.DO.data_generator(old_data, "1", [2])
            self.DO.write(self.DO.MAX14916_CONFIG1_REG, command)

    def disable_FiltrLong (self):
        """Select short blanking time (4ms) for fault bits"""
        old_data = self.DO.read(self.DO.MAX14916_CONFIG1_REG)[8:16]
        if old_data[2] == "1":
            command = self.DO.data_generator(old_data, "0", [2])
            self.DO.write(self.DO.MAX14916_CONFIG1_REG, command)

    def enable_FaultLatch (self):
        """Enable fault latching feature"""
        old_data = self.DO.read(self.DO.MAX14916_CONFIG1_REG)[8:16]
        if old_data[1] == "0":
            command = self.DO.data_generator(old_data, "1", [1])
            self.DO.write(self.DO.MAX14916_CONFIG1_REG, command)

    def disable_FaultLatch (self):
        """Disable fault latching feature"""
        old_data = self.DO.read(self.DO.MAX14916_CONFIG1_REG)[8:16]
        if old_data[1] == "1":
            command = self.DO.data_generator(old_data, "0", [1])
            self.DO.write(self.DO.MAX14916_CONFIG1_REG, command)

    def enable_SYNCH_WD (self):
        """Enable SYNCH watchdog timeout"""
        old_data = self.DO.read(self.DO.MAX14916_CONFIG2_REG)[8:16]
        if old_data[6] == "0":
            command = self.DO.data_generator(old_data, "1", [6])
            self.DO.write(self.DO.MAX14916_CONFIG2_REG, command)

    def disable_SYNCH_WD (self):
        """Disable SYNCH watchdog timeout"""
        old_data = self.DO.read(self.DO.MAX14916_CONFIG2_REG)[8:16]
        if old_data[6] == "1":
            command = self.DO.data_generator(old_data, "0", [6])
            self.DO.write(self.DO.MAX14916_CONFIG2_REG, command)

    def enable_VDD_ON_Thr (self):
        """Use VDD_GOOD_R (16V typ) threshold after UVLO event"""
        old_data = self.DO.read(self.DO.MAX14916_CONFIG2_REG)[8:16]
        if old_data[7] == "0":
            command = self.DO.data_generator(old_data, "1", [7])
            self.DO.write(self.DO.MAX14916_CONFIG2_REG, command)

    def disable_VDD_ON_Thr (self):
        """Use UVLO_VDD_R (9V typ) threshold after UVLO event"""
        old_data = self.DO.read(self.DO.MAX14916_CONFIG2_REG)[8:16]
        if old_data[7] == "1":
            command = self.DO.data_generator(old_data, "0", [7])
            self.DO.write(self.DO.MAX14916_CONFIG2_REG, command)

    def set_WD_To (self, SPI_Watchdog_To):
        """Set SPI and SYNCH watchdog Timeout"""
        if SPI_Watchdog_To not in ["0ms","200ms","600ms","1.2s"]:
            print("SPI watchdog timeout must be 0ms, 200ms, 600ms, or 1.2ms")
            return

        old_data = self.DO.read(self.DO.MAX14916_CONFIG2_REG)[8:16]
        if SPI_Watchdog_To == "0ms":
            command = self.DO.data_generator(old_data, "00", [1,0])
            self.DO.write(self.DO.MAX14916_CONFIG2_REG, command)
        if SPI_Watchdog_To == "200ms":
            command = self.DO.data_generator(old_data, "01", [1,0])
            self.DO.write(self.DO.MAX14916_CONFIG2_REG, command)
        if SPI_Watchdog_To == "600ms":
            command = self.DO.data_generator(old_data, "10", [1,0])
            self.DO.write(self.DO.MAX14916_CONFIG2_REG, command)
        if SPI_Watchdog_To == "1.2s":
            command = self.DO.data_generator(old_data, "11", [1,0])
            self.DO.write(self.DO.MAX14916_CONFIG2_REG, command)

    def set_OWOff_Cs (self, current_val):
        """Set the current source magnitude for OW detection"""
        if current_val not in ["20uA","100uA","300uA","600uA"]:
            print("Open-Wire current sense must be 20uA, 100uA, 300uA, or 600uA")
            return

        old_data = self.DO.read(self.DO.MAX14916_CONFIG2_REG)[8:16]
        if current_val == "20uA":
            command = self.DO.data_generator(old_data, "00", [3,2])
            self.DO.write(self.DO.MAX14916_CONFIG2_REG, command)
        if current_val == "100uA":
            command = self.DO.data_generator(old_data, "01", [3,2])
            self.DO.write(self.DO.MAX14916_CONFIG2_REG, command)
        if current_val == "300uA":
            command = self.DO.data_generator(old_data, "10", [3,2])
            self.DO.write(self.DO.MAX14916_CONFIG2_REG, command)
        if current_val == "600uA":
            command = self.DO.data_generator(old_data, "11", [3,2])
            self.DO.write(self.DO.MAX14916_CONFIG2_REG, command)

    def set_ShtVDD_Thr (self, voltage_thr):
        """Set the Short to VDD voltage threshold"""
        if voltage_thr not in ["9v","10v","12v","14v"]:
            print("Short to VDD sense threshold must be 9v, 10v, 12v, or 14v")
            return

        old_data = self.DO.read(self.DO.MAX14916_CONFIG2_REG)[8:16]
        if voltage_thr == "9v":
            command = self.DO.data_generator(old_data, "00", [4,5])
            self.DO.write(self.DO.MAX14916_CONFIG2_REG, command)
        if voltage_thr == "10v":
            command = self.DO.data_generator(old_data, "01", [4,5])
            self.DO.write(self.DO.MAX14916_CONFIG2_REG, command)
        if voltage_thr == "12v":
            command = self.DO.data_generator(old_data, "10", [4,5])
            self.DO.write(self.DO.MAX14916_CONFIG2_REG, command)
        if voltage_thr == "14v":
            command = self.DO.data_generator(old_data, "11", [4,5])
            self.DO.write(self.DO.MAX14916_CONFIG2_REG, command)

    def masking(self, bit, enable = 1):
        """Select register bit to enable or disable fault masking""" 
        old_data = self.DO.read(self.DO.MAX14916_MASK_REG)[8:16]
        if enable == 1:
            command = self.DO.data_generator(old_data, "1", [7-bit])
            self.DO.write(self.DO.MAX14916_MASK_REG, command)
        else: 
            command = self.DO.data_generator(old_data, "0", [7-bit])
            self.DO.write(self.DO.MAX14916_MASK_REG, command)

