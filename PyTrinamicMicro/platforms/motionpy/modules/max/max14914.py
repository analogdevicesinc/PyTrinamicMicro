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
    def __init__(self):
        self.DO_SET     =   Pin(Pin.cpu.A5,Pin.OUT_PP)
        self.DO_PP      =   Pin(Pin.cpu.A6, Pin.OUT_PP)
        self.DI_ENA     =   Pin(Pin.cpu.A7, Pin.OUT_PP)

        self.DIDO_LVL   =   Pin(Pin.cpu.C0 , Pin.IN)
        self.FAULT      =   Pin(Pin.cpu.C1, Pin.IN)
        self.OV_VDD     =   Pin(Pin.cpu.A4, Pin.IN)

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
