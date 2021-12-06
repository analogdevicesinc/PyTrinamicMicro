'''
This file implements a basic class for the MAX22005 ic as well as 
a basic implementaion to use the module MAX22005PMB.

Created on 11.3.2021

@author: KA
'''

from pyb import Pin, SPI
from PyTrinamicMicro.platforms.motionpy2.connections.spi_ic_interface import spi_ic_interface
import time
import struct

class  MAX22005(object):
    '''This class provides basic functions to use the MAX14906, for further details refer to the data sheet.'''
    #GEN Registers
    MAX22005_GEN_PROD_adr=0x00          #Product Code R
    MAX22005_GEN_REV_adr=0x01           #Revision ID code R
    MAX22005_GEN_CNFG_adr=0x02          #General Confguration R&W
    MAX22005_GEN_CHNLCTRL_adr=0x03      #General Channel Control R&W
    MAX22005_GEN_GPIOCTRL_adr=0x04      #GPIO Control R&W
    MAX22005_GEN_GPIINT_adr=0x05        #GPIO Edge Detection Control R&W 
    MAX22005_GEN_GPIDATA_adr=0x06       #GPIO Edge Detection and Logic Level R&C 
    MAX22005_GEN_INT_adr=0x07           #Interrupts R&C 
    MAX22005_GEN_INTEN_adr=0x08         #Interrupt Enable R&W
    MAX22005_GEN_PWRCTRL_adr=0x09       #Power Control  R&W 
    
    #DCHNL Registers
    MAX22005_DCHNL_CMD_adr=0x20         #DCHNL Mode R&W 
    MAX22005_DCHNL_STA_adr=0x21         #ADC Status R
    MAX22005_DCHNL_CTRL1_adr=0x22       #DCHNL Control 1 R&W
    MAX22005_DCHNL_CTRL2_adr=0x23       #DCHNL Control 2 R&W 
    MAX22005_DCHNL_DATA_adr=0x24        #DCHNL Data R 
    MAX22005_DCHNL_NSEL_adr=0x25        #DCHNL Channel Select R&W 
    MAX22005_DCHNL_NSOC_adr=0x26        #DCHNL System Offset Calibration R&W 
    MAX22005_DCHNL_NSGC_adr=0x27        #DCHNL system Gain Calibration R&W 

    CRC_ENABLE = False
    MAX22005_DS = {0, 1, 2, 3}
    MAX22005_single = {1, 3, 4, 6, 7, 9, 10, 12}
    MAX22005_diff = {"1-2", "3-4", "7-8", "7-8", "9-10"}
    MAX22005_mix = {"1-2", "1-3", "4-5", "4-6", "7-8", "7-9", "10-11", "10-12"}
    MAX22005_GPIO_mode = {"voltage":0, "current":1}
    R_SENSE = 49.9

    def __init__(self, cs = Pin.cpu.A4, spi= 1):
        Pin(cs).value(1)
        self.__SPI = spi_ic_interface(spi=SPI(spi, SPI.MASTER, baudrate=10000, polarity=0, phase=0), cs=cs)  

    def build_byte_array(self,addr, rw, data = "000000000000000000000000"):
        """returns bytearray with addr, read/write, data and crc"""
        TX_byte = "{:08b}".format((addr),8)[1:] + str(rw)
        if self.CRC_ENABLE == False:
            bits = TX_byte + data 
            send = bytearray(struct.pack("BBBB",int(bits[:8],2), int(bits[8:16],2), int(bits[16:24],2), int(bits[24:32],2)))
        elif rw == 1:
            bits = TX_byte + data + "00000000"
            send = bytearray(struct.pack("BBBBB",int(bits[:8],2), int(bits[8:16],2), int(bits[16:24],2), int(bits[24:32],2), int(bits[32:],2)))
        elif rw == 0:
            crc8 = self.generate_CRC_decode(TX_byte, data[:8], data[8:16], data[16:])
            bits = TX_byte + data + crc8
            send = bytearray(struct.pack("BBBBB",int(bits[:8],2), int(bits[8:16],2), int(bits[16:24],2), int(bits[24:32],2), int(bits[32:],2)))
        return send 

    def bin_from_recv(self,buf):
        """returns 0/1 string equivalent from send/receive buf"""
        if self.CRC_ENABLE == True:
            return '{:08b}'.format(buf[0]) + '{:08b}'.format(buf[1]) + '{:08b}'.format(buf[2]) + '{:08b}'.format(buf[3]) + '{:08b}'.format(buf[4]) 
        else: 
            return '{:08b}'.format(buf[0]) + '{:08b}'.format(buf[1]) + '{:08b}'.format(buf[2]) + '{:08b}'.format(buf[3])

    def read(self, addr):
        """sending read request and returns 24 bits 0/1 string"""
        buf_send = self.build_byte_array(addr,1)
        buf_recv = buf_send
        self.__SPI.send_recv(buf_send,buf_recv)
        read_return = self.bin_from_recv(buf_recv)

        if self.CRC_ENABLE == True:
            #verify CRC
            TX_byte = "{:08b}".format((addr),8)[1:] + '1'
            byte1 = read_return[8:16]
            byte2 = read_return[16:24]
            byte3 = read_return[24:32]
            byte_crc = read_return[32:]
            calculated_crc = self.generate_CRC_decode(TX_byte, byte1, byte2, byte3) #calculate new CRC value from returned buf
            if calculated_crc == byte_crc: #checks only calculated with returned CRC 
                return read_return
            else:
                print("Return buf: ", read_return)
                print("Calculated CRC: ", calculated_crc)
                print("Received CRC: ", byte_crc)
                print("Err: CHECK CRC ")
                return read_return
        return read_return[:32] 

    def write(self, addr, data = "000000000000000000000000"):
        """writing data provided as 0/1 string to addr. returns full receive as string"""
        buf = self.build_byte_array(addr,0, data)
        self.__SPI.send_recv(buf,buf)
        read_return = self.bin_from_recv(buf)
        return read_return 
            
    def generate_CRC_decode(self, TX_byte, byte1, byte2, byte3):
        """Calculates crc5encode decode"""
        TX_byte_int = int(TX_byte, 2)
        byte1_int = int(byte1, 2)
        byte2_int = int(byte2, 2)
        byte3_int = int(byte3,2)


        #calculate crc8decode
        crc8_start = 0 #0x00
        crc8_poly = 140 #0x8c
        crc_result = crc8_start 
        
        #TX_byte
        for i in range(0, 8):
            if (((TX_byte_int >> i)^crc_result) & 1) > 0 : 
                crc_result = (crc8_poly ^ (crc_result>>1))
            else: 
                crc_result = (crc_result>>1) 

        #Byte 1
        for i in range(0, 8):
            if (((byte1_int >> i)^crc_result) & 1) > 0 : 
                crc_result = (crc8_poly ^ (crc_result>>1))
            else: 
                crc_result = (crc_result>>1) 

        #Byte 2 
        for i in range(0, 8):
            if (((byte2_int >> i)^crc_result) & 1) > 0 : 
                crc_result = (crc8_poly ^ (crc_result>>1))
            else: 
                crc_result = (crc_result>>1)

        #Byte 3 
        for i in range(0, 8):
            if (((byte3_int >> i)^crc_result) & 1) > 0 : 
                crc_result = (crc8_poly ^ (crc_result>>1))
            else: 
                crc_result = (crc_result>>1)
        
            
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

class  MAX22005PMB(object):
    '''This class provides basic functions to use the MAX22005PMB, for further details refer to the data sheet.'''
    spi=1
    def __init__(self, **kwargs):
        time.sleep(0.2)
        if "pin_INTB" in kwargs:
            self.__IntB = Pin(kwargs["pin_INTB"], Pin.IN)
        if  "pin_READYB" in kwargs: 
            self.__ReadyB =  Pin(kwargs["pin_READYB"], Pin.IN) 
        if  "pin_RST" in kwargs: #configure synch pin as out
            self.__Rst =  Pin(kwargs["pin_RST"], Pin.OUT)
            self.__Rst.value(1)
        if  "pin_SYNCH" in kwargs: #configure enable pin as out
            self.__Synch =  Pin(kwargs["pin_SYNCH"], Pin.OUT)
            self.__Synch.value(0)  
        if "spi" in kwargs:
            spi = kwargs["spi"]   
            if  "pin_cs" in kwargs: 
                self.ADC = MAX22005(kwargs["pin_cs"],spi) #initialize object
                self.ADC.write(self.ADC.MAX22005_GEN_GPIOCTRL_adr, "000011110000111100000000") #configure GPIO 0, 1, 2, 3 to output 
                
    def interrupt(self): 
        """Returns INTB signal status"""
        return self.__IntB.value()

    def synch(self, val):
        """Control SYNCH pin as high (1) or low (0)."""
        self.__Synch.value(val)  
    
    def control_CRC(self, enable = "enable"):
        """Enable or disable CRC"""
        if self.ADC.CRC_ENABLE == False and enable == "enable":
            old_data = self.ADC.read(self.ADC.MAX22005_GEN_CNFG_adr)[8:32]
            new_data = self.ADC.data_generator(old_data, "1", [0])
            self.ADC.write(self.ADC.MAX22005_GEN_CNFG_adr, new_data)
            self.ADC.CRC_ENABLE = True
            return "CRC Enabled" 
        elif self.ADC.CRC_ENABLE == True and enable == "disable":
            old_data = self.ADC.read(self.ADC.MAX22005_GEN_CNFG_adr)[8:32]
            new_data = self.ADC.data_generator(old_data, "0", [0])
            self.ADC.write(self.ADC.MAX22005_GEN_CNFG_adr, new_data)
            self.ADC.CRC_ENABLE = False
            return "CRC Disabled" 
        
    def control_timeout(self, enable = "enable"):
        """Enable or disable watchdog timer"""
        if enable == "enable":
            old_data = self.ADC.read(self.ADC.MAX22005_GEN_CNFG_adr)[8:32]
            new_data = self.ADC.data_generator(old_data, "1", [19])
            self.ADC.write(self.ADC.MAX22005_GEN_CNFG_adr, new_data)
            return "Timeout Enabled" 
        elif enable == "disable":
            old_data = self.ADC.read(self.ADC.MAX22005_GEN_CNFG_adr)[8:32]
            new_data = self.ADC.data_generator(old_data, "0", [19])
            self.ADC.write(self.ADC.MAX22005_GEN_CNFG_adr, new_data)
            return "Timeout Disabled"

    def config_interrupt(self, interrupt, enable = "enable"):
        """Enable or disable interrupt"""
        if interrupt not in {"TMOUT","HVDD", "CNFG", "CRC", "GPI"}:
            print("ERR: Invalid interupt configuration. Select: TMOUT, HVDD, CNFG, CRC or GPI")
            return 
        else:
            bit = "1"
            if enable == "disable":
                bit = "0"
            old_data = self.ADC.read(self.ADC.MAX22005_GEN_INTEN_adr)[8:32]
            if interrupt == "TMOUT":
                new_data = self.ADC.data_generator(old_data, bit, [14])
            elif interrupt == "HVDD":
                new_data = self.ADC.data_generator(old_data, bit, [16])
            elif interrupt == "CNFG":
                new_data = self.ADC.data_generator(old_data, bit, [21])
            elif interrupt == "CRC":
                new_data = self.ADC.data_generator(old_data, bit, [22])
            elif interrupt == "GPI":
                new_data = self.ADC.data_generator(old_data, bit, [23])
            return self.ADC.write(self.ADC.MAX22005_GEN_INTEN_adr, new_data)
    
    def read_interrupt(self):
        """Return interrupt bits from interrupt register"""
        data = self.ADC.read(self.ADC.MAX22005_GEN_INT_adr)[8:32]
        return data[14] + data[16] + data[21] + data[22] + data[23]

    def reset(self):
        """Reset MAX22005"""
        self.__Rst.value(0)
        self.__Rst.value(1)

    def control_SW(self, SW, bit): 
        """Configure GPIO 0, 1, 2, 3, or 4 output high or output low"""        
        if SW not in self.ADC.MAX22005_DS:
            print("ERR: Invalid Switch. Select: 0, 1, 2, 3 ")
            return 
        else: 
            old_data = self.ADC.read(self.ADC.MAX22005_GEN_GPIOCTRL_adr)[8:32]
            new_data = self.ADC.data_generator(old_data, str(bit), [23-SW])
            self.ADC.write(self.ADC.MAX22005_GEN_GPIOCTRL_adr, new_data)
            return 

    def config_mode(self, AI_DCHNL_SEL):
        """Configure mode for analog inputs. See MAX22005 datasheet Table 5 and app note ___ for valid modes"""
        old_data = self.ADC.read(self.ADC.MAX22005_GEN_CHNLCTRL_adr)[8:32]
        new_data = self.ADC.data_generator(old_data, AI_DCHNL_SEL, [11, 12, 13, 14, 15])
        write_return = self.ADC.write(self.ADC.MAX22005_GEN_CHNLCTRL_adr, new_data)
        return write_return 

    def single_ended_voltage(self, analog_input):
        """Given analog_input (1, 3, 4, 6, 7, 9, 10, 12), configures AI as single-ended"""
        if analog_input not in self.ADC.MAX22005_single:
            print("ERR: Invalid AI channel.")
            return 
        else: 
            if analog_input == 1: 
                self.control_SW(0, 0)
            elif analog_input == 4: 
                self.control_SW(1, 0)
            elif analog_input == 7: 
                self.control_SW(2, 0)
            elif analog_input == 10: 
                self.control_SW(3, 0)
            data = str(bin(analog_input))[2:]
            #zero pad to 5 bits 
            for i in range(5-len(data)):
                data = "0" + data
            return self.config_mode(data)
    
    def diff(self, analog_inputs, mode):
        """Configure analog inputs differentially for current only: 1-2, 7-8
        Configure analog inputs differentially for voltage and current: 3-4, 9-10"""
        if analog_inputs not in self.ADC.MAX22005_diff:
            print("ERR: Invalid selection. Select: 1-2, 3-4, 7-8, 9-10.")
            return 
        else: 
            if analog_inputs == "1-2": 
                self.control_SW(0, self.ADC.MAX22005_GPIO_mode[mode])
                data = "01100"
            elif analog_inputs == "3-4": 
                self.control_SW(1, self.ADC.MAX22005_GPIO_mode[mode])
                data = "01101"
            elif analog_inputs == "7-8": 
                self.control_SW(2, self.ADC.MAX22005_GPIO_mode[mode])
                data = "01111"
            elif analog_inputs == "9-10": 
                self.control_SW(3, self.ADC.MAX22005_GPIO_mode[mode])
                data = "10000" 
            return self.config_mode(data)

    def multi_diff(self, analog_inputs, mode):
        """Configure analog inputs as multifunctional differential mode for current only: 1-2, 4-5, 7-8, 10-11
        Voltage and current: 1-3, 4-6, 7-9, 10-12"""
        if analog_inputs not in self.ADC.MAX22005_mix:
            print("ERR: Invalid AI channels.")
            return
        elif mode == "voltage" and analog_inputs in {"1-2", "4-5", "7-8", "10-11"}:
            print("ERR: Invalid AI channels. Select: 1-3, 4-6, 7-9, or 10-12")
        else:
            if analog_inputs == "1-3": 
                self.control_SW(0, self.ADC.MAX22005_GPIO_mode[mode])
                data = "10011"
            elif analog_inputs == "1-2": 
                self.control_SW(1, self.ADC.MAX22005_GPIO_mode[mode])
                data = "10010"
            elif analog_inputs == "4-5": 
                self.control_SW(1, self.ADC.MAX22005_GPIO_mode[mode])
                data = "10100"
            elif analog_inputs == "4-6": 
                self.control_SW(1, self.ADC.MAX22005_GPIO_mode[mode])
                data = "10101"
            elif analog_inputs == "7-8": 
                self.control_SW(1, self.ADC.MAX22005_GPIO_mode[mode])
                data = "10110"
            elif analog_inputs == "7-9": 
                self.control_SW(2, self.ADC.MAX22005_GPIO_mode[mode])
                data = "10111"
            elif analog_inputs == "10-11": 
                self.control_SW(1, self.ADC.MAX22005_GPIO_mode[mode])
                data = "11000"
            elif analog_inputs == "10-12": 
                self.control_SW(3, self.ADC.MAX22005_GPIO_mode[mode])
                data = "11001" 
            return self.config_mode(data)

    def set_conversion(self, conversion_type):
        """Set conversion type to continuous, single, or continous single"""
        if conversion_type not in {"continuous", "single", "continuous/single"}:
            print("ERR: Invalid conversion type. Select: continuous, single, continuous/single")
            return 
        else: 
            old_data = self.ADC.read(self.ADC.MAX22005_DCHNL_CTRL1_adr)[8:32]
            if conversion_type == "continuous":
                data = '00'
            elif conversion_type == "single":
                data = '10'
            elif conversion_type == "continuous/single":
                data = '11'
            new_data = self.ADC.data_generator(old_data, data, [6,7])
            return self.ADC.write(self.ADC.MAX22005_DCHNL_CTRL1_adr, new_data)

    def start_conversion(self, data_rate = "0000"):
        """Starts conversion at chosen data rate. See tables 7, 8, and 9 in MAX22005 datasheet for valid data rate codes."""
        old_data = self.ADC.read(self.ADC.MAX22005_DCHNL_CMD_adr)[8:32]
        new_data = self.ADC.data_generator(old_data, "11" + data_rate, [2, 3, 4, 5, 6, 7])
        self.ADC.write(self.ADC.MAX22005_DCHNL_CMD_adr, new_data)
        return 

    def stop_conversion(self):
        """Stops conversion"""
        old_data = self.ADC.read(self.ADC.MAX22005_DCHNL_CMD_adr)[8:32]
        new_data = self.ADC.data_generator(old_data, "01", [2, 3])
        return self.ADC.write(self.ADC.MAX22005_DCHNL_CMD_adr, new_data)
        
    def read_ADC(self):
        """Read ADC and returns decimal form"""
        data = self.ADC.read(self.ADC.MAX22005_DCHNL_DATA_adr)[8:32] #two's compliment form
        #print("Read ADC = ", data)
        #convert data to int
        data_int = int(data, 2) 
        if data[0] == '1': #if negative 
            V = -1 * (int(''.join('1' if x == '0' else '0' for x in data),2) +1)
        else: 
            V = data_int #return as is
    
        V = 0.00000149*V + 0.000975557
        return V
