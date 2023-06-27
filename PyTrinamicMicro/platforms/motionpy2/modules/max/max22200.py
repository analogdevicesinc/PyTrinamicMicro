"""
This file implements a basic class for the MAX22200 IC as well as
a basic implementaion to use the module MAX22200PMB#.
Created on 2022.09.27
@author: ET
"""

import time
import struct
from pyb import Pin, SPI
from PyTrinamicMicro.platforms.motionpy2.connections.spi_ic_interface import spi_ic_interface

class MAX22200(object):
    """This class provides basic functions to use the MAX22200, for further details refer to the datasheet"""
    MAX22200_STATUS_adr = 0x00      # Channel Activation/Hardware Config
    MAX22200_CFGCH0_adr = 0x01      # Configure Channel 0
    MAX22200_CFGCH1_adr = 0x02      # Configure Channel 1
    MAX22200_CFGCH2_adr = 0x03      # Configure Channel 2
    MAX22200_CFGCH3_adr = 0x04      # Configure Channel 3
    MAX22200_CFGCH4_adr = 0x05      # Configure Channel 4
    MAX22200_CFGCH5_adr = 0x06      # Configure Channel 5
    MAX22200_CFGCH6_adr = 0x07      # Configure Channel 6
    MAX22200_CFGCH7_adr = 0x08      # Configure Channel 7
    MAX22200_FAULT_adr = 0x09       # Fault Register
    MAX22200_CFGDPM_adr = 0x0A      # Detection of Plunger Movement
    MAX22200_CHANNEL = {0, 1, 2, 3, 4, 5, 6, 7}
    MAX22200_BRIDGE = {"half", "parallel", "full"}
    MAX22200_FCHOP = {0.25, 0.33, 0.5, 1}

    def __init__(self, cs = Pin.cpu.A4, spi= 1):
        Pin(cs).value(1)
        self.__SPI = spi_ic_interface(spi=SPI(spi, SPI.MASTER, baudrate=10000, polarity=0, phase=0), cs=cs)

    def read_32bit(self):
        """Returns 32 bits read from the register in a 0/1 string"""
        buf = bytearray(4)
        self.__SPI.send_recv(buf,buf)
        read_return = "{:08b}".format(buf[0]) + "{:08b}".format(buf[1]) + "{:08b}".format(buf[2]) + "{:08b}".format(buf[3])
        return read_return

    def write_8bit(self, data = "00000000"):
        """Writes 8 bits of data provided as 0/1 string"""
        buf = bytearray(struct.pack("B", int(data, 2)))
        self.__SPI.send_recv(buf,buf)
        return data

    def write_32bit(self, data = "00000000000000000000000000000000"):
        """Writes 32 bits of data provided as 0/1 string"""
        buf = bytearray(struct.pack("BBBB", int(data[:8], 2), int(data[8:16], 2), int(data[16:24], 2), int(data[24:], 2)))
        self.__SPI.send_recv(buf,buf)
        return data

    def write_command_reg(self, rw, addr, msb):
        """Writes 8 bits of data provided as 0/1 string to command register"""
        command = str(rw) + "00" + "{:04b}".format(addr) + str(msb)
        buf = bytearray(struct.pack("B", int(command, 2)))
        self.__SPI.send_recv(buf,buf)
        print("Write to Command Register: ", command)
        return

class MAX22200PMB(object):
    """This class provides basic functions to use the MAX22200PMB#, for further details refer to the datasheet"""
    spi = 1
    def __init__(self, **kwargs):
        time.sleep(0.2)
        if "pin_fault" in kwargs: # Configure fault pin as input
            self.__Fault = Pin(kwargs["pin_fault"], Pin.IN)
        if "pin_command" in kwargs:  # Configure command pin as output
            self.__Command = Pin(kwargs["pin_command"], Pin.OUT)
        if "pin_enable" in kwargs: # Configure enable pin as output
            self.__Enable = Pin(kwargs["pin_enable"], Pin.OUT)
            self.__Enable.value(1)
        if "pin_trig" in kwargs: # Configure trig pin as output
            self.__Trig = Pin(kwargs["pin_trig"], Pin.OUT)
            self.__Trig.value(0)
        while self.__Enable.value() == 0:
            time.sleep(0.1)
            print("Not Ready")
        if "spi" in kwargs:
            spi = kwargs["spi"]
            if  "pin_cs" in kwargs:
                self.PMB = MAX22200(kwargs["pin_cs"], spi) # Initialize object

    """Status Register Fault Flag Bits [7:0]"""
    def status_reg_flags(self):
        """Reads and prints fault flag bits in status register"""
        self.__Command.value(1)
        self.PMB.write_command_reg(0, self.PMB.MAX22200_STATUS_adr, 0) # Write to command reg to prepare to read status reg
        self.__Command.value(0)
        read = self.PMB.read_32bit()[24:] # Read fault flags in status reg
        print("Fault Flags: ", read)
        return read

    """Status Register"""
    def status_reg(self, M_OVT, M_OCP, M_OLF, M_HHF, M_DPM, M_COM, M_UVM, FREQM, ch7_6, ch5_4, ch3_2, ch1_0, active):
        """Set parameters for status register"""
        mask_freq = str(M_OVT) + str(M_OCP) + str(M_OLF) + str(M_HHF) + str(M_DPM) + str(M_COM) + str(M_UVM)
        if FREQM == "100kHz":
            mask_freq = mask_freq + "0"
        elif FREQM == "80kHz":
            mask_freq = mask_freq + "1"
        else:
            print("ERROR: Please select valid frequency")

        hw_config = "00000000"
        config = dict({
            "half": "00",
            "parallel": "01",
            "full": "10"
        })

        if all(x in self.PMB.MAX22200_BRIDGE for x in [ch7_6, ch5_4, ch3_2, ch1_0]):  # returns True if all inputs are valid
            hw_config = config[ch7_6] + config[ch5_4] + config[ch3_2] + config[ch1_0]
        else:
            print("ERROR: Invalid input, defaulting to all half-bridge configurations")

        send = "0000000" + str(active) + str(hw_config) + str(mask_freq) + "00000000"
        self.__Command.value(1)
        self.PMB.write_command_reg(1, self.PMB.MAX22200_STATUS_adr, 0)
        self.__Command.value(0)
        self.PMB.write_32bit(send)
        print("Write to Register: ", send)
        return

    """Configuration Register"""
    def config_reg(self, channel, HFS, HOLD, TRGnSPI, HIT, HIT_time, VDRnCDR, HSnLS, FREQ_CFG, SRC, OL, DPM, HHF):
        """Configure each channel, can also be used 'on-the-fly'"""
        ch = ""
        if channel not in self.PMB.MAX22200_CHANNEL:
            print("ERROR: Please select valid channel")
        else:
            ch = channel + 1

        hold_curr = "{:07b}".format(HOLD)
        hit_curr = "{:07b}".format(HIT)
        hit_time = "{:08b}".format(HIT_time)

        freq = ""
        if FREQ_CFG == 0.25:
            freq = "00"
        elif FREQ_CFG == 0.33:
            freq = "01"
        elif FREQ_CFG == 0.5:
            freq = "10"
        elif FREQ_CFG == 1:
            freq = "11"
        else:
            print("ERROR: Please select valid chopping value")

        byte = str(VDRnCDR) + str(HSnLS) + str(freq) + str(SRC) + str(OL) + str(DPM) + str(HHF)
        send = byte + hit_time + str(TRGnSPI) + hit_curr + str(HFS) + hold_curr
        self.__Command.value(1)
        self.PMB.write_command_reg(1, ch, 0)
        self.__Command.value(0)
        self.PMB.write_32bit(send)
        print("Write to Register: ", send)

        if TRGnSPI == 1: # External trigger
            self.__Trig.value(1)
        else: # SPI trigger
            self.__Trig.value(0)

        return

    """Read Output Channel Register"""
    def read_output(self, channel):
        """Returns contents of register for selected output"""
        ch = channel + 1
        self.__Command.value(1)
        self.PMB.write_command_reg(0, ch, 0)
        self.__Command.value(0)
        print("Read Channel: ", self.PMB.read_32bit())
        return

    """Fault Register"""
    def read_faults(self):
        """Returns all seven channels' faults as 0/1 string (CH0 is LSB)"""
        self.__Command.value(1)
        self.PMB.write_command_reg(0, self.PMB.MAX22200_FAULT_adr, 0) # Write to command reg to prepare to read fault reg
        self.__Command.value(0)
        fault = self.PMB.read_32bit()
        OCP = fault[:8]
        HHF = fault[8:16]
        OLF = fault[16:24]
        DPM = fault[24:]
        print("Channels:                       76543210")
        print("Overcurrent Protection:        ", OCP)
        print("HIT Current Not Reached:       ", HHF)
        print("Open-Load Detection:           ", OLF)
        print("Detection of Plunger Movement: ", DPM)
        return

    """DPM Register"""
    def CFG_DPM(self, DPM_ISTART, DPM_TDEB, DPM_ITPH, HFS, FREQM, FREQ_CFG):
        """Set parameters for detection of plunger movement, only available in CDR mode. HFS/FREQM/FREQ_CFG bits only used for calculations, does not actually set bits"""
        reserved = "0000000000000000"
        start = "{:07b}".format(DPM_ISTART)
        debounce = "{:04b}".format(DPM_TDEB)
        threshold = "{:04b}".format(DPM_ITPH)

        send = debounce + threshold + "0" + start + reserved
        self.__Command.value(1)
        self.PMB.write_command_reg(1, self.PMB.MAX22200_CFGDPM_adr, 0)
        self.__Command.value(0)
        self.PMB.write_32bit(send)
        print("Write to Register: ", send)

        main_freq = ""
        if FREQM == "100kHz":
            main_freq = 100000
        elif FREQM == "80kHz":
            main_freq = 80000
        else:
            print("ERROR: Please set FREQM to either '100kHz' or '80kHz'")

        Fchop = ""
        if FREQ_CFG not in self.PMB.MAX22200_FCHOP:
            print("ERROR: Please select valid chopping value")
        else:
            Fchop = main_freq * FREQ_CFG

        if HFS == 0:
            print("Starting Current (A): ", DPM_ISTART/127)
            print("DPM Debouncer (s): ", DPM_TDEB/Fchop)
            print("DPM Threshold (A): ", DPM_ITPH/127)
        elif HFS == 1:
            print("Starting Current (A): ", DPM_ISTART * 0.5/127)
            print("DPM Debouncer (s): ", DPM_TDEB/Fchop)
            print("DPM Threshold (A): ", DPM_ITPH * 0.5/127)

        return

    """Update 'On-The-Fly'"""
    def channel_on_off_spi(self, channel, status):
        """Turn each channel on/off on the fly via SPI"""
        self.__Command.value(1)
        self.PMB.write_command_reg(0, self.PMB.MAX22200_STATUS_adr, 0)
        self.__Command.value(0)
        data = self.PMB.read_32bit()[:8]
        print("Channel [7:0] Current Status: ", data)

        send = ""
        if channel not in self.PMB.MAX22200_CHANNEL:
            print("ERROR: Please select valid channel")
        else: # splits string at index of channel and replaces value with user value
            i = len(data) - channel - 1
            str1 = data[:i]
            str2 = data[i+1:]
            send = str1 + str(status) + str2

        self.__Command.value(1)
        self.PMB.write_command_reg(1, self.PMB.MAX22200_STATUS_adr, 1)
        self.__Command.value(0)
        self.PMB.write_8bit(send)
        print("Channel [7:0] New Status: ", send)
        return

    def channel_on_off_trig(self, status):
        """Turn channel on/off on the fly via TRIGA/B"""
        if status == 1: # Turn channel(s) on
            self.__Trig.value(1)
        else: # Turn channel(s) off
            self.__Trig.value(0)
        return

    def HFS_HOLD(self, channel, HFS, HOLD):
        """Adjust HFS bit and HOLD current on the fly"""
        ch = ""
        if channel not in self.PMB.MAX22200_CHANNEL:
            print("ERROR: Please select valid channel")
        else:
            ch = channel + 1

        send = str(HFS) + "{:07b}".format(HOLD)
        self.__Command.value(1)
        self.PMB.write_command_reg(1, ch, 1)
        self.__Command.value(0)
        self.PMB.write_8bit(send)
        print("Write to Register: ", send)
        return

    def channel_config(self, channel, HFS, HOLD, TRGnSPI, HIT, HIT_time, VDRnCDR, HSnLS, FREQ_CFG, SRC, OL, DPM, HHF):
        """Adjust other register parameters and turn channel off and back on. Not all parameters can be adjusted on-the-fly,
        refer to datasheet for full details."""
        if TRGnSPI == 1: # External trigger
            self.config_reg(channel, HFS, HOLD, TRGnSPI, HIT, HIT_time, VDRnCDR, HSnLS, FREQ_CFG, SRC, OL, DPM, HHF)
            self.__Trig.value(0)
            self.__Trig.value(1)
        else: # SPI trigger
            self.config_reg(channel, HFS, HOLD, TRGnSPI, HIT, HIT_time, VDRnCDR, HSnLS, FREQ_CFG, SRC, OL, DPM, HHF)
            self.channel_on_off_spi(channel, 0)
            self.channel_on_off_spi(channel, 1)
        return