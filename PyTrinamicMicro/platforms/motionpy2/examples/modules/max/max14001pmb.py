'''
Example using the MAX14001PMB

Created on 27.01.2021

@author: JH
'''

from PyTrinamicMicro.platforms.motionpy2.modules.max.max14001 import MAX14001, MAX14001PMB
from pyb import Pin
import time
import logging

# Prepare Logger
logger = logging.getLogger(__name__)
logger.info("Reading ADC values")

pmod0 = dict({
    "pin_cs_volt"   : Pin.cpu.C6,
    "pin_cs_curr"   : Pin.cpu.A4, 
    "pin_cout_volt" : Pin.cpu.B0,
    "pin_cout_curr" : Pin.cpu.C13,
    "pin_fault"     : Pin.cpu.C5,
    "spi" : 1
    })

pmod1 = dict({
    "pin_cs_volt"   : Pin.cpu.C2,
    "pin_cs_curr"   : Pin.cpu.B12, 
    "pin_cout_volt" : Pin.cpu.C4,
    "pin_cout_curr" : Pin.cpu.C7,
    "pin_fault"     : Pin.cpu.C3,
    "spi" : 2
    })

'''Change pmod connector here'''
connector = pmod0

max14001pmb = MAX14001PMB(**connector)
filtered = True
max14001pmb.set_cout_volt(18,20)
max14001pmb.set_cout_curr(0.4,0.5)
print("Readout of MAX14001:")
while(True):
    for cursor in '|/-\\':
        currV = max14001pmb.get_voltage(filtered)
        currI = max14001pmb.get_current(filtered)
        coutV = max14001pmb.get_cout_volt()
        coutI  = max14001pmb.get_cout_curr()
        fault = max14001pmb.get_fault()
        text =  cursor+" U:" +  "{:10.4f}".format(currV) + "V; I: " + "{:10.4f}".format(currI)+ "A; comp. U: " + str(coutV)+ "; comp. I: " + str(coutI) + "; fault: " + str(fault)
        print(text, end='\r')
        time.sleep(0.1)
