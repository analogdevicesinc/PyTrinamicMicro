'''
Example using the MAX22005PMB

Created on 13.10.2021

@author: KA
'''
#Paste into terminal to run: exec(open("PyTrinamicMicro/platforms/motionpy2/examples/modules/max/max22005pmb.py").read())

from PyTrinamicMicro.platforms.motionpy2.modules.max.max22005 import MAX22005, MAX22005PMB
from pyb import Pin
import time
import logging

# Prepare Logger
logger = logging.getLogger(__name__)
logger.info("Reading ADC")

pmod0 = dict({
    "pin_cs"            : Pin.cpu.A4,
    "pin_INTB"         : Pin.cpu.C6,
    "pin_READYB"         : Pin.cpu.B0,
    "pin_RSTB"        : Pin.cpu.C13,
    "pin_SYNCH"         : Pin.cpu.C5,
    "spi" : 1
    })

pmod1 = dict({
    "pin_cs"            : Pin.cpu.B12,
    "pin_INTB"         : Pin.cpu.C2, 
    "pin_READYB"         : Pin.cpu.C4,
    "pin_RSTB"        : Pin.cpu.C6,
    "pin_SYNCH"         : Pin.cpu.C3,
    "spi" : 2
    })

'''Change pmod connector here'''
connector = pmod0
max22005pmb = MAX22005PMB(**connector)

#test script to communicate with PMB

#configure device 
max22005pmb.control_CRC("enable") #enable crc 

#single ended measurement
#max22005pmb.single_ended_voltage(1) #measure single ended voltage

#differential measurements 
#max22005pmb.diff("1-2", "current") #differential current 
#max22005pmb.diff("3-4", "voltage") #measure differential voltage 

#multifunctual differential measurements
#max22005pmb.multi_diff("1-3", "current") #measure multifunctual differential current 
max22005pmb.multi_diff("1-3", "voltage") #measure multifunctual differential voltage

#configure ADC conversion
max22005pmb.set_conversion("continuous")
max22005pmb.start_conversion()

while(True): 
    for cursor in '|/-\\':
        #wait until sample ready 
        while(max22005pmb.__ReadyB.value() == 1):

        voltage = max22005pmb.read_ADC() 
        #current = (voltage/49.9)*2000 #current in mA

        print(cursor + " V = ", voltage, end='\r')







