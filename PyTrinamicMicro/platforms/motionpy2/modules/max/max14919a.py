'''
This file implements all functions for MAX14919A.

Created on 07.13.2022

@author: MJC
'''
from pyb import Pin 
import time


class MAX14919A:
    
    def __init__(self, CH1_IN = Pin.cpu.A4, CH2_IN = Pin.cpu.A7, CH3_IN = Pin.cpu.A6, CH4_IN = Pin.cpu.A5, INRUSH_pin = Pin.cpu.C6, FAULT_pin = Pin.cpu.B0, REV_pin = Pin.cpu.C13):
        self.CH1_IN     =   Pin(CH1_IN,Pin.OUT, None)
        self.CH1_IN.value(0) #Had trouble properly initializing the Pin.OUTs so manually setting
        self.CH2_IN     =   Pin(CH2_IN,Pin.OUT, None)
        self.CH2_IN.value(0)
        self.CH3_IN     =   Pin(CH3_IN,Pin.OUT, None)
        self.CH3_IN.value(0)
        self.CH4_IN     =   Pin(CH4_IN,Pin.OUT, None)
        self.CH4_IN.value(0)
        self.INRUSH     =   Pin(INRUSH_pin, Pin.OUT, None) #Initial condition of 0 to disable on startup
        self.INRUSH.value(0)

        self.FAULT      =   Pin(FAULT_pin, Pin.IN, None)
        self.REV        =   Pin(REV_pin, Pin.IN)

    def setCH(self,CH):
        ''' set CH1-4 high '''
        if(CH == 1):
            self.CH1_IN.value(1)
        elif(CH == 2):
            self.CH2_IN.value(1)
        elif(CH == 3):
            self.CH3_IN.value(1)
        elif(CH == 4):
            self.CH4_IN.value(1)
        else:
            print("Invalid input, input 1-4 for channels")

    def setINRUSHmode(self, mode):
        ''' Set INRUSH high or low '''
        if(mode == 0):
            self.INRUSH.value(0) #Disable INRUSH"
        elif(mode == 1):
            self.INRUSH.value(1) #Enable INRUSH"
        else:
            print("Invalid input, input 0 to disable or 1 to enable")

    def clearCH(self,CH):
        ''' set CH1-4 low '''
        if(CH == 1):
            self.CH1_IN.value(0)
        elif(CH == 2):
            self.CH2_IN.value(0)
        elif(CH == 3):
            self.CH3_IN.value(0)
        elif(CH == 4):
            self.CH4_IN.value(0)
        else:
            print("Invalid input, input 1-4 for channels")

    def getFAULT(self):
        ''' get value of FAULT pin '''
        return self.FAULT.value()

    def getREV(self):
        return self.REV.value()
