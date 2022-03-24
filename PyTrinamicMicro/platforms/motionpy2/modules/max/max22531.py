'''
This file implements a basic class for the MAX22531 ic as well as 
a basic implementaion to use the module MAX22531PMB.
Created on 27.11.2021
@author: ABN
'''

from pyb import Pin, SPI
from PyTrinamicMicro.platforms.motionpy2.connections.spi_ic_interface import spi_ic_interface
import time
import struct

class  MAX22531(object):
    '''This class provides basic functions to use the MAX22531, for further details refer to the data sheet.'''
    PROD_ID_adr=0x00               #Device Product ID Register, Read Only 
    ADC1_adr=0x01                  #ADC1 Register, Read Only 
    ADC2_adr= 0x02                 #ADC2 Register, Read Only  
    ADC3_adr=0x03                  #ADC3 Register, Read Only 
    ADC4_adr=0x04                  #ADC4 Register, Read Only  
    FADC1_adr=0x05                 #Filtered ADC1 Register, Read Only 
    FADC2_adr=0x06                 #Filtered ADC2 Register, Read Only
    FADC3_adr=0x07                 #Filtered ADC3 Register, Read Only
    FADC4_adr=0x08                 #Filtered ADC4 Register, Read Only
    COUTHI1_adr=0x09               #Comparator1 Higher Threshold, R&W 
    COUTHI2_adr=0x0a               #Comparator2 Higher Threshold, R&W 
    COUTHI3_adr=0x0b               #Comparator3 Higher Threshold, R&W
    COUTHI4_adr=0x0c               #Comparator4 Higher Threshold, R&W
    COUTLO1_adr=0x0d               #Comparator1 Lower Threshold, R&W
    COUTLO2_adr=0x0e               #Comparator2 Lower Threshold, R&W
    COUTLO3_adr=0x0f               #Comparator3 Lower Threshold, R&W
    COUTLO4_adr=0x10               #Comparator4 Lower Threshold, R&W
    COUT_STATUS_adr=0x11           #COUT1-4 Output Status Register, Read Only
    INTERRUPT_STATUS_adr=0x12      #Interrupt Status Register, Read Only
    INTERRUPT_ENABLE_adr=0x13      #Interrupt Enable Register, R&W
    CONTROL_adr=0x14               #Control Register, R&W
    CRC_ENABLE = False
    CRCTable = bytearray(256)

    def __init__(self, cs = Pin.cpu.A4, spi= 1):
        self.__SPI = spi_ic_interface(spi=SPI(spi, SPI.MASTER, baudrate=10000, polarity=0, phase=0), cs=cs)
        self.buildCRCTable()
        """if cout:
            self.__COUT1 = Pin(cout1, Pin.IN)
            self.__COUT2 = Pin(cout2, Pin.IN)"""
            
    """def rev(self, s):
        returns inverse of string s  
        return "" if not(s) else self.rev(s[1::])+s[0]  """      

    def build_byte_array(self,addr, rw, burst, data = "0000000000000000"):
        """returns bytearray with addr, read/write, burst, data and crc"""
        TX_byte = "{:08b}".format((addr),6)[2:] + str(rw) + str(burst)
        if self.CRC_ENABLE == False:
            bits = TX_byte + data 
            if(burst == 0):
                send = bytearray(struct.pack("BBB",int(bits[:8],2), int(bits[8:16],2), int(bits[16:24],2)))
            else:
                bits = bits + "0000000000000000000000000000000000000000000000000000000000000000"
                send = bytearray(struct.pack("BBBBBBBBBBB",int(bits[:8],2), int(bits[8:16],2), int(bits[16:24],2), int(bits[24:32],2), int(bits[32:40],2), int(bits[40:48],2), int(bits[48:56],2), int(bits[56:64],2), int(bits[64:72],2), int(bits[72:80],2), int(bits[80:88],2)))
        elif self.CRC_ENABLE == True:
            crc8 = self.generate_CRC_decode(TX_byte, data[:8], data[8:16])
            if(burst == 0):
                bits = TX_byte + data + "{:08b}".format((crc8))
                send = bytearray(struct.pack("BBBB",int(bits[:8],2), int(bits[8:16],2), int(bits[16:24],2), int(bits[24:32],2)))
            else:
                bits = TX_byte + data + "000000000000000000000000000000000000000000000000000000000000000000000000"
                send = bytearray(struct.pack("BBBBBBBBBBBB",int(bits[:8],2), int(bits[8:16],2), int(bits[16:24],2), int(bits[24:32],2), int(bits[32:40],2), int(bits[40:48],2), int(bits[48:56],2), int(bits[56:64],2), int(bits[64:72],2), int(bits[72:80],2), int(bits[80:88],2), int(bits[88:96],2)))
        return send 

    def bin_from_recv(self,buf):
        """returns 0/1 string equivalent from send/receive buf"""
        if self.CRC_ENABLE == True:
            return '{:08b}'.format(buf[0]) + '{:08b}'.format(buf[1]) + '{:08b}'.format(buf[2]) + '{:08b}'.format(buf[3]) 
        else: 
            return '{:08b}'.format(buf[0]) + '{:08b}'.format(buf[1]) + '{:08b}'.format(buf[2]) 
 
    def burst_bin_from_recv(self,buf):
        #""" returns 0/1 string equivalent from send/receive buff from burst read operation """ 		
        if self.CRC_ENABLE == True:
            return '{:08b}'.format(buf[0]) + '{:08b}'.format(buf[1]) + '{:08b}'.format(buf[2]) + '{:08b}'.format(buf[3]) + '{:08b}'.format(buf[4]) + '{:08b}'.format(buf[5]) + '{:08b}'.format(buf[6]) + '{:08b}'.format(buf[7]) + '{:08b}'.format(buf[8]) + '{:08b}'.format(buf[9]) + '{:08b}'.format(buf[10]) + '{:08b}'.format(buf[11]) 
        else: 
            return '{:08b}'.format(buf[0]) + '{:08b}'.format(buf[1]) + '{:08b}'.format(buf[2]) + '{:08b}'.format(buf[3]) + '{:08b}'.format(buf[4]) + '{:08b}'.format(buf[5]) + '{:08b}'.format(buf[6]) + '{:08b}'.format(buf[7]) + '{:08b}'.format(buf[8]) + '{:08b}'.format(buf[9]) + '{:08b}'.format(buf[10])	

    def data_from_recv(self,buf):
        """extracts data from receive, returns string"""
        return self.rev(self.bin_from_recv(buf))[6:]

    def int_from_data(self,data):
        """returns integer from 0/1 string"""
        return int(data,2)

    def read(self, addr):
        """sending read request and returns 16 bits 0/1 string"""
        buf_send = self.build_byte_array(addr,0,0)
        buf_recv = buf_send
        self.__SPI.send_recv(buf_send,buf_recv)
        read_return = self.bin_from_recv(buf_recv)
        #return self.data_from_recv(buf_recv)
        if self.CRC_ENABLE == True:
            #verify CRC
            TX_byte = "{:08b}".format((addr),8)[2:]+str(0)+str(0)
            byte1 = read_return[8:16]
            byte2 = read_return[16:24]
            byte_crc = read_return[24:]
            calculated_crc = self.generate_CRC_decode(TX_byte, byte1, byte2) # calculate new CRC value for received information from recieved buf
            if calculated_crc == int(byte_crc,2): #checks calculated CRC to returned CRC from device
                return read_return
            else:
                print("Return Buffer: ", read_return)
                print("Calculated CRC: ", calculated_crc)
                print("Received CRC: ", byte_crc)
                print("Err: CHECK CRC ")
                return read_return
        return read_return[:24]

    def Burst_read(self,addr):
        #""" sending burst read request and returns 16bit strings of burst read settings ADC(1-4)/FADC(1-4), INTERRUPT_STATUS """
        buf_send = self.build_byte_array(addr,0,1)
        buf_recv = buf_send
        self.__SPI.send_recv(buf_send,buf_recv)
        read_return = self.burst_bin_from_recv(buf_recv)
        if self.CRC_ENABLE == True:
            #verify CRC
            TX_byte = "{:08b}".format((addr),8)[2:]+str(0)+str(1)
            byte1 = read_return[8:16]
            byte2 = read_return[16:24]			
            byte3 = read_return[24:32]
            byte4 = read_return[32:40]
            byte5 = read_return[40:48]
            byte6 = read_return[48:56]
            byte7 = read_return[56:64]
            byte8 = read_return[64:72]
            byte9 = read_return[72:80]
            byte10 = read_return[80:88]
            byte_crc = read_return[88:]
            calculated_crc = self.generate_burst_CRC_decode(TX_byte, byte1, byte2, byte3, byte4, byte5, byte6, byte7, byte8, byte9, byte10) # calculate new CRC value for received information from received buffer
            if (calculated_crc == int(byte_crc,2)): #checks calculated CRC to returned CRC from device
                return read_return
            else:
                print("Return Buffer: ", read_return)
                print("Calculated CRC: ", calculated_crc)
                print("Received CRC: ", byte_crc)
                print("Err: CHECK CRC ")
                return read_return
        return read_return[:88]			
       
    def write(self, addr, data = "0000000000"):
        """writing data provided as 0/1 string to addr. returns full receive as string"""
        buf = self.build_byte_array(addr,1,0, data)
        self.__SPI.send_recv(buf,buf)
        read_return = self.bin_from_recv(buf)
        return read_return

    def data_bits_change(self, old_data, new_data, location):
        """changes specified bis in old data with new data"""
        list_data = list(old_data)
        for i in range(0,len(location)):
            list_data[location[i]] = new_data[i]
        old_data = "".join(list_data)
        return old_data

    
    def generate_CRC_decode(self, TX_byte, byte1, byte2):
        #"""Calculates crc encode decode"""
        frame_high = int(TX_byte,2)
        frame_mid = int(byte1,2)
        frame_low = int(byte2,2)
        message = [frame_high, frame_mid, frame_low]
        crc_value = int(self.getCRC(message,3))
        return crc_value

    def generate_burst_CRC_decode(self, TX_byte, byte1, byte2, byte3, byte4, byte5, byte6, byte7, byte8, byte9, byte10):
        #"""Calculates crc encode decode"""
        frame_1 = int(TX_byte,2)
        frame_2 = int(byte1,2)
        frame_3 = int(byte2,2)
        frame_4 = int(byte3,2)
        frame_5 = int(byte4,2)
        frame_6 = int(byte5,2)
        frame_7 = int(byte6,2)
        frame_8 = int(byte7,2)
        frame_9 = int(byte8,2)
        frame_10 = int(byte9,2)
        frame_11 = int(byte10,2)
        message = [frame_1, frame_2, frame_3,frame_4, frame_5, frame_6, frame_7, frame_8, frame_9, frame_10, frame_11]
        crc_value = int(self.getCRC(message,11))
        return crc_value

    def getCRC(self,message, length):
        crc_value = 0
        for k in range(0,length):
           crc_value = self.CRCTable[crc_value ^ message[k]]
        return crc_value    

    def buildCRCTable(self):
        for i in range(0,256):
            self.CRCTable[i] = self.getCRCforByte(i)

    def getCRCforByte(self,i):
        CRC_POLY = 7 #0x07
        for j in range(0,8):
            if((i & 128) == 128):
                i = (i << 1)^CRC_POLY
            else:
                i = (i << 1)
        return i%256


        
        
        
class  MAX22531PMB(object):
    '''This class provides basic functions to use the MAX22531PMB, for further details refer to the data sheet.'''
    CH1_FACTOR = 0.36
    CH2_FACTOR = 0.36
    CH3_FACTOR = 0.36
    CH4_FACTOR = 0.36
    VOLT_FACTOR = 0.666
    VOLT_OFFSET = 0
    MAX22531_ID = 129
    FACTOR = 0
    COMP_UPPER_THRESHOLD_adr = False
    COMP_LOWER_THRESHOLD_adr = False
    CH_adr = False
    #self.buildCRCTable()

    spi=1
    def __init__(self, **kwargs):
        time.sleep(0.1)
        if "pin_INTB" in kwargs:
            self.__IntB = Pin(kwargs["pin_INTB"], Pin.IN)
        if  "pin_COUT1" in kwargs: 
            self.__Cout1 =  Pin(kwargs["pin_COUT1"], Pin.IN) 
        if  "pin_COUT2" in kwargs: 
            self.__Cout2 =  Pin(kwargs["pin_COUT2"], Pin.IN)           
        if "spi" in kwargs:
            spi = kwargs["spi"] 
            if  "pin_cs" in kwargs: 
                self.ADC = MAX22531(kwargs["pin_cs"],spi) #initialize object
            
    def intb_interrupt(self):
        """returns INTB signal status"""
        return self.__IntB.value()

    def read_cout1(self):
        """Returns COUT1 signal status"""
        return self.__Cout1.value()

    def read_cout2(self):
        """Returns COUT1 signal status"""
        return self.__Cout2.value()

    def Control_CRC(self, enable = "enable"):
        #"""Enable or Disable CRC"""
        if self.ADC.CRC_ENABLE == False and enable == "enable":
            old_data = self.ADC.read(self.ADC.CONTROL_adr)[8:24]
            new_data = self.ADC.data_bits_change(old_data,"1",[0])
            self.ADC.write(self.ADC.CONTROL_adr, new_data)
            self.ADC.CRC_ENABLE = True
            return "CRC Enabled"
        elif self.ADC.CRC_ENABLE == True and enable == "disable":
            old_data = self.ADC.read(self.ADC.CONTROL_adr)[8:24]
            new_data = self.ADC.data_bits_change(old_data,"0",[0])
            self.ADC.write(self.ADC.CONTROL_adr, new_data)
            self.ADC.CRC_ENABLE = False
            return "CRC Disabled"
        elif self.ADC.CRC_ENABLE == True and enable == "enable":
            return "CRC is Enabled"

    def Configure_Interrupt(self, interrupt, enable = "enable"):
        #"""Enable/ Disable Interrupts in Interrupt enable register"""
        if interrupt not in {"EEOC","EFADC","EFLD","ESPIFRM","ESPICRC","ECO_POS_4","ECO_POS_3","ECO_POS_2","ECO_POS_1", "ECO_NEG_4","ECO_NEG_3","ECO_NEG_2","ECO_NEG_1"}:
            print("ERR: Invalid Interrupt Enable Configuration. Select: EEOC, EFADC, EFLD, ESPIFRM, ESPICRC, ECO_POS_4, ECO_POS_3, ECO_POS_2, ECO_POS_1, ECO_NEG_4, ECO_NEG_3, ECO_NEG_2 or ECO_NEG_1")
            return
        else:
            bit = "1"
            if enable == "disable":
                bit = "0"
            old_data = self.ADC.read(self.ADC.INTERRUPT_ENABLE_adr)[8:24]
            if interrupt == "EEOC":
                new_data = self.ADC.data_bits_change(old_data, bit, [3])
            elif interrupt == "EFADC":
                new_data = self.ADC.data_bits_change(old_data, bit, [4])
            elif interrupt == "EFLD":
                new_data = self.ADC.data_bits_change(old_data, bit, [5])
            elif interrupt == "ESPIFRM":
                new_data = self.ADC.data_bits_change(old_data, bit, [6])
            elif interrupt == "ESPICRC":
                new_data = self.ADC.data_bits_change(old_data, bit, [7])
            elif interrupt == "ECO_POS_4":
                new_data = self.ADC.data_bits_change(old_data, bit, [8])
            elif interrupt == "ECO_POS_3":
                new_data = self.ADC.data_bits_change(old_data, bit, [9])
            elif interrupt == "ECO_POS_2":
                new_data = self.ADC.data_bits_change(old_data, bit, [10])
            elif interrupt == "ECO_POS_1":
                new_data = self.ADC.data_bits_change(old_data, bit, [11])
            elif interrupt == "ECO_NEG_4":
                new_data = self.ADC.data_bits_change(old_data, bit, [12])
            elif interrupt == "ECO_NEG_3":
                new_data = self.ADC.data_bits_change(old_data, bit, [13])
            elif interrupt == "ECO_NEG_2":
                new_data = self.ADC.data_bits_change(old_data, bit, [14])
            elif interrupt == "ECO_NEG_1":
                new_data = self.ADC.data_bits_change(old_data, bit, [15])
            return self.ADC.write(self.ADC.INTERRUPT_ENABLE_adr, new_data)

    def device_init(self):
        status = 1
        if(int(self.ADC.read(self.ADC.PROD_ID_adr)[8:24],2) != self.MAX22531_ID):
            status = 0
        data = list(self.ADC.read(self.ADC.CONTROL_adr)[8:24])
        bit_crc = data[0]
        if(bit_crc == "1"):
            self.ADC.CRC_ENABLE = True
            self.Control_CRC("disable")
        return status

    def read_interrupt(self):
        """Returns interrupt bits from Interrupt Status Register"""
        data = self.ADC.read(self.ADC.INTERRUPT_STATUS_adr)[8:24]
        return data[3] + data[4] + data[5] + data[6] + data[7] + data[8] + data[9] + data[10] + data[11] + data[12] + data[13] + data[14] + data[15] 
        
    def reset(self):
        """Hard Resets the Device"""
        self.ADC.write(self.ADC.CONTROL_adr, "0000000000000001")

    def comparator_modes_inputSelect(self, Channel, mode, input_select):
        """Configures COTHI(1-4) operation mode and input selection"""
        if(Channel == 1):
            self.CH_adr = self.ADC.COUTHI1_adr
        elif(Channel == 2):
            self.CH_adr = self.ADC.COUTHI2_adr
        elif(Channel == 3):
            self.CH_adr = self.ADC.COUTHI3_adr
        elif(Channel == 4):
            self.CH_adr = self.ADC.COUTHI4_adr
        else:
            print("Err: Choose Channel 1 to 4 to configure associated comparator upper and lower threshold values")
            return
           
        if(mode == 0):
            old_data = self.ADC.read(self.CH_adr)[8:24]
            temp_data = self.ADC.data_bits_change(old_data,"0",[0])                        
        elif(mode == 1):
            old_data = self.ADC.read(self.CH_adr)[8:24]
            temp_data = self.ADC.data_bits_change(old_data,"1",[0])
        else:
            print("Err: Set Operation Mode bit CO_MODE to either 0 or 1")
            return
        if(input_select == 0):
            new_data = self.ADC.data_bits_change(temp_data,"0",[1])
        elif(input_select == 1):
            new_data = self.ADC.data_bits_change(temp_data,"1",[1])
        else:
            print("Err: Set Input select Mode bit CO_IN_SEL to either 0 or 1")
            return
        self.ADC.write(self.CH_adr, new_data)   
 

    def set_comparator_thres_volt(self, Channel, lower_value, upper_value):
        '''set the threshold for voltage comparator with Voltage inputs'''
        if (lower_value >= upper_value):
            print("Err: Comparator Lower Threshold register value cannot be higher than Upper Threshold")
            return
        else:
            if(Channel == 1):
                self.FACTOR = self.CH1_FACTOR
                self.COMP_UPPER_TRESHOLD_adr = self.ADC.COUTHI1_adr
                self.COMP_LOWER_TRESHOLD_adr = self.ADC.COUTLO1_adr
            elif(Channel == 2):
                self.FACTOR = self.CH2_FACTOR
                self.COMP_UPPER_TRESHOLD_adr = self.ADC.COUTHI2_adr
                self.COMP_LOWER_TRESHOLD_adr = self.ADC.COUTLO2_adr
            elif (Channel == 3):
                self.FACTOR = self.CH3_FACTOR
                self.COMP_UPPER_TRESHOLD_adr = self.ADC.COUTHI3_adr
                self.COMP_LOWER_TRESHOLD_adr = self.ADC.COUTLO3_adr
            elif (Channel == 4):
                self.FACTOR = self.CH4_FACTOR
                self.COMP_UPPER_TRESHOLD_adr = self.ADC.COUTHI4_adr
                self.COMP_LOWER_TRESHOLD_adr = self.ADC.COUTLO4_adr
            else:
                print("Err: Choose Channel 1 to 4 to configure associated comparator upper and lower threshold values")
                return
            
            lower_value_scaled = ((lower_value+self.VOLT_OFFSET)*self.FACTOR )*4096/1.8
            upper_value_scaled = ((upper_value+self.VOLT_OFFSET)*self.FACTOR )*4096/1.8
            comp_config_data = self.ADC.read(self.COMP_UPPER_TRESHOLD_adr)[8:24]
            mode = (list(comp_config_data))[0]
            inpt_select = (list(comp_config_data))[1]
            
            self.ADC.write(self.COMP_LOWER_TRESHOLD_adr, "{:016b}".format(round(lower_value_scaled)))
            self.ADC.write(self.COMP_UPPER_TRESHOLD_adr, (str(mode)+str(inpt_select)+"{:014b}".format(round(upper_value_scaled))))


    def set_comparator_thres_hex(self, Channel, lower_value, upper_value):
        '''set the threshold for voltage comparator with hex inputs'''
        if (lower_value >= upper_value):
            print("Err: Comparator Lower Threshold register value cannot be higher than Upper Threshold")
            return
        else:
            if(Channel == 1):
                self.FACTOR = self.CH1_FACTOR
                self.COMP_UPPER_TRESHOLD_adr = self.ADC.COUTHI1_adr
                self.COMP_LOWER_TRESHOLD_adr = self.ADC.COUTLO1_adr
            elif(Channel == 2):
                self.FACTOR = self.CH2_FACTOR
                self.COMP_UPPER_TRESHOLD_adr = self.ADC.COUTHI2_adr
                self.COMP_LOWER_TRESHOLD_adr = self.ADC.COUTLO2_adr
            elif (Channel == 3):
                self.FACTOR = self.CH3_FACTOR
                self.COMP_UPPER_TRESHOLD_adr = self.ADC.COUTHI3_adr
                self.COMP_LOWER_TRESHOLD_adr = self.ADC.COUTLO3_adr
            elif (Channel == 4):
                self.FACTOR = self.CH4_FACTOR
                self.COMP_UPPER_TRESHOLD_adr = self.ADC.COUTHI4_adr
                self.COMP_LOWER_TRESHOLD_adr = self.ADC.COUTLO4_adr
            else:
                print("Err: Choose Channel 1 to 4 to configure associated comparator upper and lower threshold values")
                return
            
            comp_config_data = self.ADC.read(self.COMP_UPPER_TRESHOLD_adr)[8:24]
            mode = (list(comp_config_data))[0]
            inpt_select = (list(comp_config_data))[1]
            
            self.ADC.write(self.COMP_LOWER_TRESHOLD_adr, "{:016b}".format(lower_value))
            self.ADC.write(self.COMP_UPPER_TRESHOLD_adr, (str(mode)+str(inpt_select)+"{:014b}".format(upper_value)))
        
    def read_ADC(self, Channel):
        #"Reads ADCx x: channel 1 to 4 and returns decimal form"""
        if(Channel == 1):
            self.CH_adr = self.ADC.ADC1_adr
            self.FACTOR = self.CH1_FACTOR
        elif(Channel == 2):
            self.CH_adr = self.ADC.ADC2_adr
            self.FACTOR = self.CH2_FACTOR
        elif(Channel == 3):
            self.CH_adr = self.ADC.ADC3_adr
            self.FACTOR = self.CH3_FACTOR
        elif(Channel == 4):
            self.CH_adr = self.ADC.ADC4_adr
            self.FACTOR = self.CH4_FACTOR
        else:
            print("Err: Choose Channel 1 to 4 to configure associated comparator upper and lower threshold values")
            return
        decimal_data = self.ADC.read(self.CH_adr)[8:24]
        voltage_data = (int(decimal_data,2) * 1.8/4096)/self.FACTOR
        return decimal_data, voltage_data
	
    def read_FADC(self, Channel):
    #"Reads ADCx x: channel 1 to 4 and returns decimal form"""
        if(Channel == 1):
            self.CH_adr = self.ADC.FADC1_adr
            self.FACTOR = self.CH1_FACTOR
        elif(Channel == 2):
            self.CH_adr = self.ADC.FADC2_adr
            self.FACTOR = self.CH2_FACTOR
        elif(Channel == 3):
            self.CH_adr = self.ADC.FADC3_adr
            self.FACTOR = self.CH3_FACTOR
        elif(Channel == 4):
            self.CH_adr = self.ADC.FADC4_adr
            self.FACTOR = self.CH4_FACTOR
        else:
            print("Err: Choose Channel 1 to 4 to configure associated comparator upper and lower threshold values")
            return
        decimal_data = self.ADC.read(self.CH_adr)[8:24]
        voltage_data = (int(decimal_data,2) * 1.8/4096)/self.FACTOR
        return decimal_data, voltage_data
		
    def read_Register(self,adr):
        return (str(adr),self.ADC.read(adr)[8:24])

    def read_COUT_Status(self):
        return (self.ADC.read(self.ADC.COUT_STATUS_adr)[20:24])

    def read_Analog_CH_COUT_Status_Cout1_Cout2(self, filtered = "false"):
    #"""Reads all 4 ADC or FADC channels, COUT Status and COUT1 and COUT2 analog comparator output channels """
    #""" When filtered = false, reads ADC1 - 4, when filtered = true, reads FADC1 - 4"""
        if(filtered == "false"):
            ADC1 = self.ADC.read(self.ADC.ADC1_adr)[8:24]
            ADC2 = self.ADC.read(self.ADC.ADC2_adr)[8:24]			
            ADC3 = self.ADC.read(self.ADC.ADC3_adr)[8:24]
            ADC4 = self.ADC.read(self.ADC.ADC4_adr)[8:24]	
        elif(filtered == "true"):
            ADC1 = self.ADC.read(self.ADC.FADC1_adr)[8:24]
            ADC2 = self.ADC.read(self.ADC.FADC2_adr)[8:24]			
            ADC3 = self.ADC.read(self.ADC.FADC3_adr)[8:24]
            ADC4 = self.ADC.read(self.ADC.FADC4_adr)[8:24]   
        else:
            print("Provide infromation for filtered option")
            return
        cout_status = self.ADC.read(self.ADC.COUT_STATUS_adr)[20:24]
        Cout1_comp = self.read_cout1()
        Cout2_comp = self.read_cout2()
        if(Cout1_comp == 1):
            print("COUT1 COMPARATOR OUTPUT STATUS ON")	
        elif(Cout2_comp == 1):
            print("COUT2 COMPARATOR OUTPUT STATUS ON")
        return ADC1, ADC2, ADC3, ADC4, cout_status, Cout1_comp, Cout2_comp

    def Burst_read(self, Channel):
        #"""if channel is ADC, Burst read (ADC), if channel is FADC, Burst read (FADC) """	
        if(Channel == "ADC"):
            burst_read = self.ADC.Burst_read(1)[8:88]
        elif(Channel == "FADC"):
            burst_read = self.ADC.Burst_read(5)[8:88]
        else:
            print("Provide infromation to burst read 'ADC' or 'FADC' ")
            return            
        return burst_read[:16],burst_read[16:32],burst_read[32:48],burst_read[48:64],burst_read[64:88]		
