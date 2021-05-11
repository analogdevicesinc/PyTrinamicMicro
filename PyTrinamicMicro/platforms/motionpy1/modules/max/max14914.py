from pyb import Pin 
import time

'''
DI_ENA defines the DOI as a digital output (set to 0) or as a digital input (set to 1).
DO_PP defines the mode of DOI, depending upon how
DI_ENA is set. If the MAX14914 is configured as a digital output, DO_PP selects high-side mode (set to 0) or pushpull mode (set to 1). 
        If the MAX14914 is configured as a digital input, DO_PP selects type 1/3 mode (set to 0) or type 2 mode (set to 1).
DO_SET is used when the MAX14914 is configured as a DO; when DO_SET is 0 the output pin DOI is either high impedance (in high-side mode) or 0V (in push-pull mode).
        When DO_SET is 1, the output pin DOI is turned on (24V) in high-side mode or in push-pull mode.
'''
class MAX14914:
    def __init__(self, do_set_pin = Pin.cpu.A5, do_pp_pin = Pin.cpu.A6, di_ena_pin = Pin.cpu.A7, dido_lvl_pin = Pin.cpu.C0, fault_pin = Pin.cpu.C1, ov_vdd_pin = Pin.cpu.A4):
        self.DO_SET     =   Pin(do_set_pin,Pin.OUT_PP)
        self.DO_PP      =   Pin(do_pp_pin, Pin.OUT_PP)
        self.DI_ENA     =   Pin(di_ena_pin, Pin.OUT_PP)

        self.DIDO_LVL   =   Pin(dido_lvl_pin , Pin.IN)
        self.FAULT      =   Pin(fault_pin, Pin.IN)
        self.OV_VDD     =   Pin(ov_vdd_pin, Pin.IN)

    def setIOMode(self,mode):
        ''' set input mode D0 = 0 or DI = 1'''
        if(mode == "0"):
                self.DI_ENA.low()
        elif(mode == "1"):
                self.DI_ENA.high()   

    #DI_ENA = HIGH
    def setPPMode(self,mode):
        ''' set input mode D0 or DI'''
        if(mode == 0):
            self.DO_PP.low()
        elif(mode == 1):
            self.DO_PP.high()   
    def setDO(self,state): 
        '''set Digital Out'''
        self.DO_SET.value(state)                       
    def getDIDO_LVL(self):
        '''get level of DOI-PIN'''
        return self.DIDO_LVL.value()
    def getFault(self):
        '''getFault'''
        return not self.FAULT.value()
    def getOV_VDD(self):
        '''reports an overvoltage detection'''
        return self.OV_VDD.value()
