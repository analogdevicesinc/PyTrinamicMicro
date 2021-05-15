'''
Example using the MAX22191PMB.
This scripts toggles output of MAX22191PMB.
Created on 9.03.2021

@author: JH
'''
from pyb import Pin
import time
import logging

logger = logging.getLogger(__name__)
logger.info("MAX22191PMB example running")


pmod0 = dict({
    "DI1"     :   Pin.cpu.A4,
    "DI2"     :   Pin.cpu.A7,
    })

pmod1 = dict({
    "DI1"     :   Pin.cpu.B12,
    "DI2"     :   Pin.cpu.B15,
    })

'''Change pmod connector here'''
connector = pmod0




DI1     =   Pin(Pin.cpu.C1,Pin.OUT_PP)
DI2     =  Pin(Pin.cpu.A7, Pin.OUT_PP)

while(True):
    for cursor in '|/-\\':
        DI1_lvl = DI1.value()
        DI2_lvl = DI2.value()
        text =  cursor+" DI1 state: " +  str(DI1_lvl) + "; DI2 state: " + str(DI2_lvl)
        print(text, end='\r')
        time.sleep(0.2)
