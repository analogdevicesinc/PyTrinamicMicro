'''
Example using the MAX22196PMB#

Created on 22-09-2022

@author: BR
'''
#Paste into terminal to run: exec(open("PyTrinamicMicro/platforms/motionpy2/examples/modules/max/max14906pmb.py").read())

from PyTrinamicMicro.platforms.motionpy2.modules.max.max22196 import MAX22196, MAX22196PMB
from pyb import Pin
import time
import logging

# Prepare Logger
logger = logging.getLogger(__name__)
logger.info("Test MAX22196PMB")

pmod1 = dict({
    "pin_cs"            : Pin.cpu.A4,
    "pin_ready"         : Pin.cpu.B0,
    "pin_latch"         : Pin.cpu.C13,
    "pin_crcen"         : Pin.cpu.C5,
    "pin_fault"         : Pin.cpu.C6,
    "spi" : 1
    })

pmod2 = dict({
    "pin_cs"            : Pin.cpu.B12,
    "pin_ready"         : Pin.cpu.C4, 
    "pin_latch"         : Pin.cpu.C7,
    "pin_crcen"         : Pin.cpu.C3,
    "pin_fault"         : Pin.cpu.C2,
    "spi" : 2
    })

'''Change pmod connector here'''
connector = pmod1
max22196pmb = MAX22196PMB(**connector)

# Change default configuration to sink mode type 1/3 for each channel
# Set HITH_ to 1 and CURR_ to 01
#print(str(max22196pmb.read_reg(str(0x03))))
#max22196pmb.write_reg(str(0x03),str(0xdc))
#print(str(max22196pmb.read_reg(str(0x03))))
max22196pmb.cnfg_channel(1,'1/3',1)
max22196pmb.cnfg_filter(1,4)

max22196pmb.LEDmatrix("auto")

# check faults
# if clear read DI states and print to console log
max22196pmb.Fault1_mask(5,0)
max22196pmb.Fault1_mask(2,0)

def latch(line):    
    time.sleep(0.5)
    print("interrupt,line: ", line)
    latch = connector["pin_latch"]
    if latch.value():
        latch.value(0)
        print("Input latched")
    else:
        latch.value(1)
        print("input un-latched")

# initialise a push button to latch the inputs
pyb.ExtInt(Pin.cpu.C0, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, latch)

while(True):
    if max22196pmb.get_ready_pin(): 
        print("not ready")
    else:
        if not max22196pmb.get_fault_pin():
            print("fault detected")
            max22196pmb.read_faults()

        else:
            max22196pmb.print_DISTATE()
            # Read DI state
    time.sleep(0.5)
