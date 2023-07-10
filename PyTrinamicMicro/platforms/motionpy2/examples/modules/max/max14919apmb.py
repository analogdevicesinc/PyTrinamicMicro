'''
Example using the MAX149149APMB.
Created on 07.15.2022

@author: MJC
'''
from pyb import Pin 
from PyTrinamicMicro.platforms.motionpy2.modules.max.max14919a import MAX14919A
import time

pmod0 = dict({
    "CH1_IN"        :   Pin.cpu.A4,
    "CH2_IN"        :   Pin.cpu.A7,
    "CH3_IN"        :   Pin.cpu.A6,
    "CH4_IN"        :   Pin.cpu.A5, 
    "INRUSH_pin"    :   Pin.cpu.C6,
    "FAULT_pin"     :   Pin.cpu.B0,
    "REV_pin"       :   Pin.cpu.C13
    })

pmod1 = dict({
    "CH1_IN"        :   Pin.cpu.B12,
    "CH2_IN"        :   Pin.cpu.B15,
    "CH3_IN"        :   Pin.cpu.B14,
    "CH4_IN"        :   Pin.cpu.B13, 
    "INRUSH_pin"    :   Pin.cpu.C2,
    "FAULT_pin"     :   Pin.cpu.C4,
    "REV_pin"       :   Pin.cpu.C3
    })

'''Change pmod connector here'''
connector = pmod0
module = MAX14919A(**connector)

for number in range (1,5):
    module.setCH(number)
    time.sleep(0.5)

for number in range (1,5):
    module.clearCH(number)
    time.sleep(0.5)

print("Reading FAULT: " + str(module.getFAULT()))
time.sleep(0.5)

print("Reading REV: " + str(module.getREV()))