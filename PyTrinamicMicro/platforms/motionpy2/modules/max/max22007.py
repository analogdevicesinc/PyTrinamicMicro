'''
Example using the MAX22007PMB

Created on 13.10.2021

@author: 
'''
############################################################################################################
"""max22007.py"""
'''
This file implements a basic class for the MAX22007 Quad Digital Output.
It also exposes a basic implementaion to use the module MAX22007PMB.

Created on 25.09.2021
'''

from pyb import Pin, SPI
from PyTrinamicMicro.platforms.motionpy2.connections.spi_ic_interface import spi_ic_interface
import time
import struct
###########################################################################################################

class MAX22007(object):
    """MAX22007 4-Channel Analog Output IC class"""
    """This class exposes basic functionality of MAX22007. For more details, refer to the IC datasheet.
    https://datasheets.maximintegrated.com/en/ds/MAX22007.pdf"""

    #REG MAP (16 bit registers)
    MAX22007_REV_adr=0x00       #Revision (Part/Rev IDs) 0x00 
    
    MAX22007_STAT_adr=0x01      #Status/Ints 
    MAX22007_INTEN_adr=0x02     #Int Enables 

    MAX22007_CFG_adr=0x03       #Config
    MAX22007_CTRL_adr=0x04      #Control
    MAX22007_MODES_adr=0x05     #Channel Mode/Power Control
    MAX22007_RST_adr=0x06       #Soft Reset (Channel Data or IC)

    MAX22007_CH0_adr=0x07       #CH0 Data 0x07
    MAX22007_CH1_adr=0x08       #CH1 Data 0x08
    MAX22007_CH2_adr=0x09       #CH2 Data 0x09
    MAX22007_CH3_adr=0x0A       #CH3 Data 0x0A

    MAX22007_GPCTRL_adr=0x0B    #GPIO Ctrl 0x0B
    MAX22007_GPDATA_adr=0x0C    #GPIO Data 0x0C
    MAX22007_EDCTRL_adr=0x0D    #GPI Edge Detection Control
    MAX22007_EDSTAT_adr=0x0E    #GPI Edge Detection Status

    #Table for computing CRC
    CRC_TABLE = (0, 94, 188, 226, 97, 63, 221, 131, 194, 156, 126, 32, 163, 253, 31, 65,
	157, 195, 33, 127, 252, 162, 64, 30, 95, 1, 227, 189, 62, 96, 130, 220,
	35, 125, 159, 193, 66, 28, 254, 160, 225, 191, 93, 3, 128, 222, 60, 98,
	190, 224, 2, 92, 223, 129, 99, 61, 124, 34, 192, 158, 29, 67, 161, 255,
	70, 24, 250, 164, 39, 121, 155, 197, 132, 218, 56, 102, 229, 187, 89, 7,
	219, 133, 103, 57, 186, 228, 6, 88, 25, 71, 165, 251, 120, 38, 196, 154,
	101, 59, 217, 135, 4, 90, 184, 230, 167, 249, 27, 69, 198, 152, 122, 36,
	248, 166, 68, 26, 153, 199, 37, 123, 58, 100, 134, 216, 91, 5, 231, 185,
	140, 210, 48, 110, 237, 179, 81, 15, 78, 16, 242, 172, 47, 113, 147, 205,
	17, 79, 173, 243, 112, 46, 204, 146, 211, 141, 111, 49, 178, 236, 14, 80,
	175, 241, 19, 77, 206, 144, 114, 44, 109, 51, 209, 143, 12, 82, 176, 238,
	50, 108, 142, 208, 83, 13, 239, 177, 240, 174, 76, 18, 145, 207, 45, 115,
	202, 148, 118, 40, 171, 245, 23, 73, 8, 86, 180, 234, 105, 55, 213, 139,
	87, 9, 235, 181, 54, 104, 138, 212, 149, 203, 41, 119, 244, 170, 72, 22,
	233, 183, 85, 11, 136, 214, 52, 106, 43, 117, 151, 201, 74, 20, 246, 168,
	116, 42, 200, 150, 21, 75, 169, 247, 182, 232, 10, 84, 215, 137, 107, 53)

    #Init function
    def __init__(self, cs=Pin.cpu.A4, spi=1, intb=Pin.cpu.C6):
        """Initialization for MAX22007 class

        Args:
            cs (Pin, optional): Chip Select pin. Defaults to Pin.cpu.A4 on PMOD1
            spi (int, optional): Spi bus. Defaults to bus 1 on PMOD1
            intb (Pin, optional): Interrupt pin. Defaults to Pin.cpu.C6 on PMOD1
        """
        self.__SPI = spi_ic_interface(spi=SPI(spi, SPI.MASTER, baudrate=100000, polarity=0, phase=0), cs=cs)
        self.__SPI.__cs.high() #Set CS to idle high.
        
        #Initialize CRC flag
        self.crc_en = 0
        temp = self.read(self.MAX22007_CFG_adr)
        if temp[15] == '0':
            self.crc_en = 0
        else:
            self.crc_en = 1


    #Data Conversions
    def build_byte_array(self,addr, rw, data = "0000000000000000"):
        """Build a byte array object from string data to write with SPI

        Args:
            addr (int): SPI register address
            rw (int): read(1) /write(0) bit
            data (str, optional): Data to write. Defaults to "0000000000000000".

        Returns:
            bytearray: packed array of binary data in bytes
        """
        
        bits = "{:08b}".format((addr)<<1)[:7] + str(rw) + data
        #inv_bits = self.reverse(bits)

        if (len(bits) > 24):
            return bytearray(struct.pack("4B", int(bits[:8], 2), int(bits[8:16], 2), int(bits[16:24], 2), int(bits[24:], 2) ))
        
        return bytearray(struct.pack("3B", int(bits[:8], 2), int(bits[8:16], 2), int(bits[16:24], 2) ))
    
    def bytes_to_string(self,buf):
        """return binary string of concatenated bytes from a buffer

        Args:
            buf (bytearray): buffer of bytes to convert to binary string

        Returns:
            str: binary data
        """
        
        temp = ""
        for i in range(len(buf)):
            temp = temp + '{:08b}'.format(buf[i])
        return temp

    #SPI Functions (read and write fully tested)
    def read(self, addr):
        """send a read request and return 16bit 0/1 string

        Args:
            addr (int): Register address

        Returns:
            str: binary data received
        """
        
        if self.crc_en == 0:
            buf_send = self.build_byte_array(addr,1)
            buf_recv = buf_send
            self.__SPI.send_recv(buf_send,buf_recv) #send read req1
            reg_data = self.bytes_to_string(buf_recv)[8:] #return data from buffer
            return reg_data
        else:
            data = "000000000000000000000000"
            buf_send = self.build_byte_array(addr, 1, data)
            buf_recv = buf_send
            self.__SPI.send_recv(buf_send, buf_recv) #gets the value
            result = self.bytes_to_string(buf_recv)
            reg_data = result[8:24]
            crc_recv = int(result[24:],2)

            byte1 = (addr << 1) + 1
            byte2 = int(reg_data[:8],2)
            byte3 = int(reg_data[8:],2)
            
            #NOTE: Operands for crc are:
            #   -Address + R/W bit
            #   -Data MSB
            #   -Data LSB
            crc = self.crc_compute([byte1,byte2,byte3])
            if (crc != crc_recv):
                print("Invalid CRC Check for reg " + '0x{:02X}.'.format(addr) + "Please read again.")
                print("Expected:" + str(crc) + ". Received:" + str(crc_recv))
            return reg_data
        
    def write(self, addr, data = "0000000000000000"):
        """SPI write function

        Args:
            addr (int): Register address to write to
            data (str, optional): Binary data to write. Defaults to "0000000000000000".
        """
        if self.crc_en == 0:
            buf = self.build_byte_array(addr,0, data)
            self.__SPI.send_recv(buf,buf)
            return
        else:
            addr_tx = (addr << 1)
            crc = self.crc_compute([addr_tx, int(data[:8], 2), int(data[8:], 2)])
            data = data + '{:08b}'.format(crc)
            buf_send = self.build_byte_array(addr,0,data)
            
            buf_recv = buf_send
            self.__SPI.send_recv(buf_send,buf_recv)
            return

    def disable_crc(self):
        """Disable CRC feature.
        """
        
        temp = self.read(self.MAX22007_CFG_adr)
        temp = temp[:15] + "0"
        recv = self.write(self.MAX22007_CFG_adr, temp)
        self.crc_en = 0
        return

    def enable_crc(self):
        """Enable CRC feature
        """
        temp = self.read(self.MAX22007_CFG_adr)
        temp = temp[:15] + "1"
        recv = self.write(self.MAX22007_CFG_adr, temp)
        self.crc_en = 1
        return

    # Returns the CRC-8 based on Maxim's CRC algorithm. For more information, please visit: 
    # https://www.maximintegrated.com/en/design/technical-documents/app-notes/2/27.html
    def crc_compute(self, buf = []):
        """Return CRC-8 of input data. Uses the lookup table method from the above article.
        Each step is next_crc = lookup[data XOR current_crc]. 

        Args:
            buf (list, optional): Data to compute CRC-8 of. Defaults to [].

        Returns:
            int: CRC-8 of input buffer.
        """
        crc = 0x00
        for byte in buf:
            crc = self.CRC_TABLE[byte^crc]
        return crc

class MAX22007PMB(object):
    """MAX22007 Pmod Board Class"""
    """This class provides basic functionality of MAX22007PMB. For further information, please see the datasheet.
    https://datasheets.maximintegrated.com/en/ds/MAX22007.pdf"""
    
    #define any constants needed here
    led_ch1_blue = 0x0100
    led_ch2_blue = 0x0200
    led_ch3_blue = 0x0400
    led_ch4_blue = 0x0800
    led_ch1_green = 0x1000
    led_ch2_green = 0x2000
    led_ch3_green = 0x4000
    led_ch4_green = 0x8000

    VOLTAGE_OFFSET = 2
    CURRENT_OFFSET = 0
    SECONDS = 1

    def __init__(self, **kwargs):
        """
            Initialization for MAX22007 objects.
            
            Args:
            kwargs: dictionary specifying spi bus ("spi"), cs pin ("pin_cs"), and intb pin ("pin_intb")
        """
        time.sleep(0.2 * self.SECONDS)

        #changes the SPI bus based on which pmod header
        if "spi" in kwargs: 
            spi = kwargs["spi"]
        else:
            spi = 1
        
        #defines a dac object, disables crc, and sets all GPIO to enabled output state
        self.dac = MAX22007(kwargs["pin_cs"], spi, kwargs["pin_intb"])
        self.dac.disable_crc()
        self.dac.write(self.dac.MAX22007_GPDATA_adr, "0000000000000000") #Clear initial GPO data.
        self.dac.write(self.dac.MAX22007_GPCTRL_adr, "1111111111111111") #Enable all GPIO ports + set to output. 
        self.dac.write(self.dac.MAX22007_CFG_adr, "1111000000000000") #Set DAC latch to transparent
        
    def set_channel_mode(self, ch, mode=0, on=1):
        """sets the mode for a channel. "0"=voltage, "1"=current.

        Args:
            ch: (int) Channel being used. Indexed 1-4.
            mode (int, optional): Voltage (0) or Current (1) mode. Defaults to 0.
            on (int, optional): Channel Enable (1) / Disable (0). Defaults to 1.

        Returns:
            [string]: binary data written
        """
        if (ch < 1) or (ch > 4):
            return "Invalid channel. Valid range is 1 to 4."
        elif (mode < 0) or (mode > 1):
            return "invalid Mode. Valid values are Voltage (0) or Current (1) mode."

        data = int(self.dac.read(self.dac.MAX22007_MODES_adr), 2)
        
        #map the input to a byte of data
            #bit 15:12 is ch3-ch0 mode
            #bit 11:8 is ch3-ch0 on/off
        if mode == 1:
            new_data = '{:016b}'.format(data | (1 << (11+ch)) )
        else:
            new_data = '{:016b}'.format(data & ~(1 << (11+ch)) )
        
        new_data = int(new_data,2)
        if on == 1:
            new_data = '{:016b}'.format(new_data | (1 << (7+ch)) )
        else:
            new_data = '{:016b}'.format(new_data & ~(1 << (7+ch)) )

        self.dac.write(self.dac.MAX22007_MODES_adr, new_data)
        return new_data

    def set_channel_data(self, ch, data = "0000000000000000"):
        """Set data for a DAC channel. 

        Args:
            ch (int): Channel to write to. Indexed 1-4.
            data (str, optional): Data to write. Defaults to "0000000000000000".
        """
        if (ch < 1) or (ch > 4) or (len(data) != 16):
            return "Invalid input params. Channel is 0 to 3, data is 16 bits."
        self.dac.write(self.dac.MAX22007_CH0_adr + (ch-1), data)
        return
        
    '''
        Equation for setting the voltage can be seen on page 21 of the MAX22007 Datasheet:
        https://datasheets.maximintegrated.com/en/ds/MAX22007.pdf
    
        Vout = Vref * D/(2^N) where N=12, D=Data, Vref=12.5 V
    
        Therefore, D = (4096)/(12.5 V) * Vout 
        VOLTAGE_OFFSET is used to calibrate from test data. It is measured in binary LSBs.
    
        Test Data: 
        10.0 -> 09.981 V (diff: 0.019 V)
        9.0 -> 08.986 V (diff: 0.014 V)
        7.5 -> 07.486 V (diff: 0.014 V)
        6.0 -> 05.989 V (diff: 0.011 V)
        5.0 -> 4.9896 V (diff: 0.0104 V)
        2.0 -> 1.9935 V (diff: 0.0065 V)
        1.0 -> 0.9939 V (diff: 0.0061 V)
        0.5 -> 0.4939 V (diff: 0.0061 V)
        Sum of diff: 0.0871
        Avg: 0.0108875 V
        Avg in closest ADC counts: int(4096 * 0.010875/12.5) = 3
        Using 2 instead to keep the lower ranges in spec.
    '''  
    def voltage_to_data(self, voltage=0.0):
        """Convert decimal voltage to binary data

        Args:
            voltage (float, optional): Voltage to convert in Volts. Defaults to 0.0.
            
        Returns:
            string: binary data representing voltage
        """
        #(bit 0to3 is reserved, 4-15 is data)
        if ((voltage < 0.0) or (voltage > 12.5)):
            return "Invalid voltage. Valid range is 0 to 12.5 V."
        if (voltage == 12.5):
            return "1111111111110000" #Fixing an issue with the binary math
        res = 12.5 / 4096
        return '{:016b}'.format(round(voltage / res) + self.VOLTAGE_OFFSET) << 4)

    '''
        Equation for setting the current can be seen on page 22 of the MAX22007 Datasheet:
        https://datasheets.maximintegrated.com/en/ds/MAX22007.pdf

        Iout = (1.25 V/ Rsense) * (D/2^N) where Rsense=49.99 Ohms,  D=Data, N=12

        Therefore...
        D = Iout * (4096 * 49.99 Ohms / 1.25 V) 
        CURRENT_OFFSET is used to calibrate from test data. It is measured in binary LSBs.

        Test Data: 
            0.10 -> 0.09 mA (diff: -0.01 mA)
            0.15 -> 0.139 (diff: -0.011 mA)
            0.50 -> 0.488 (diff: -0.012 mA)
            1.00 -> 0.991 (diff: -0.009 mA)
            2.50 -> 2.499 (diff: -0.001 mA)
            5.00 -> 5.011 (diff: +0.011 mA)
            10.0 -> 10.033 (diff: +0.031 mA)
            15.0 -> 15.054 (diff: +0.054 mA)
            20.0 -> 20.077 (diff: +0.077 mA)
            25.0 -> 25.100 (diff: +0.103 mA)
            Sum: +0.233 mA
            Avg: +0.0233 mA
            Avg in counts: 0.0233 mA / ((1.25/49.99) / 4096) [denom is LSB: 6.104736572314463 uAmps]
                = 3.8167 --> 3
        It was found that adding offset brought the lower values out of spec.
        Since the device will be used mostly for light loads (small current),
        the offset will be 0 for current.
    '''
    def current_to_data(self, current=0.000):
        """Convert decimal current to binary data

        Args:
            current (float, optional): Current to convert in Amps. Defaults to 0.000.
                                        Range of 0.000-0.025 A.

        Returns:
            string: binary data for current
        """
        #(bit 0to3 is reserved, 4-15 is data)
        if ((current < 0.0) or (current > 0.025)):
            return "Invalid current. Valid range is 0.000 to 0.025 A."
        
        #round data to nearest lsb
        data = (round(current * (4096*49.99/1.25)) + self.CURRENT_OFFSET) << 4) 
        return '{:016b}'.format(data)

    def set_channel_voltage(self, ch, voltage = 0.0):
        """Set voltage for an individual channel.

        Args:
            ch (int): Channel to set (1-4)
            voltage (float, optional): Voltage to set channel to in Volts. Defaults to 0.0.
        """
        if ((ch < 1) or (ch > 4) or (ch is None)):
            return "Invalid channel. 1 to 4 is valid."
        
        #Read the channel modes register
        temp = self.dac.read(self.dac.MAX22007_MODES_adr)
        mode = temp[4-ch]
        on = temp[8-ch]

        #Make sure the channel is enabled and in voltage mode
        if not ((mode == "0") and (on == "1")):
            self.set_channel_mode(ch, 0, 1)

        #Set the channel data
        self.set_channel_data(ch, self.voltage_to_data(voltage))
        return 

    def set_channel_current(self, ch, current=0.0):
        """Set the current for an individual channel.

        Args:
            ch ([type]): Channel to set (1-4)
            current (float, optional): Current to set channel to in Amps. Defaults to 0.0000000.
        """
        
        if ((ch < 1) or (ch > 4) or (ch is None)):
            return "Invalid channel. 1 to 4 is valid."
        
        #Read the channel modes register
        temp = self.dac.read(self.dac.MAX22007_MODES_adr)
        mode = temp[3-ch]
        on = temp[8-ch]

        #Make sure the channel is enabled and in current mode
        if not ((mode == "1") and (on == "1")):
            self.set_channel_mode(ch, 1, 1)

        #Set the channel data
        self.set_channel_data(ch, self.current_to_data(current))
        return

    def set_LED(self, ch, mode=0):
        """Set an LED for a channel

        Args:
            ch (int): Channel to set (1-4)
            mode (int, optional): Voltage (0) or current (1) mode. Defaults to 0.
        """
        if ((ch < 1) or (ch > 4) or (ch is None)):
            return "Invalid channel. 1 to 4 is valid."

        reg_data = int(self.dac.read(self.dac.MAX22007_GPDATA_adr), 2)

        if (mode == 0): #Voltage mode = blue 
            reg_data = '{:016b}'.format(reg_data | (1 << (7 + ch)))
        elif (mode == 1): #Current mode = green
            reg_data = '{:016b}'.format(reg_data | (1 << (11+ch)))
        else:
            return "Invalid Mode. 0 = Voltage, 1 = Current."
        self.dac.write(self.dac.MAX22007_GPDATA_adr, reg_data)
        return
    
    def clear_LED(self, ch, mode=0):
        """Clear an LED for a channel

        Args:
            ch (int): Channel to clear (1-4)
            mode (int, optional): Voltage (0) or current (1) mode. Defaults to 0.
        """
        
        if ((ch < 1) or (ch > 4)):
            return "Invalid channel. 1 to 4 is valid."

        reg_data = int(self.dac.read(self.dac.MAX22007_GPDATA_adr), 2)

        #Bit 15:8 is GPO. GPI is 7:0. 
        if (mode == 0):
            reg_data = '{:016b}'.format(reg_data & ~(1 << (7 + ch) ))
        elif (mode == 1):
            reg_data = '{:016b}'.format(reg_data & ~(1 << (11 + ch)))
        else:
            return "Invalid Mode. 0 = Voltage, 1 = Current."

        self.dac.write(self.dac.MAX22007_GPDATA_adr, reg_data)
        return

"""END OF max22007.py"""