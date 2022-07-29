'''
Example using the MAX14916PMB.
This script turns on all the switches, and then enables the open-wire fault detection for cahnnels
1 and 2, and then reports the open-wire faults. 
Created on 19.07.2022

@author: TL
'''

#Paste into terminal to run: exec(open("PyTrinamicMicro/platforms/motionpy2/examples/modules/max/max14916pmb_example.py").read())

import time
from pyb import Pin
from  PyTrinamicMicro.platforms.motionpy2.modules.max.max14916 import MAX14916PMB

#For readability
SECONDS = 1

#Pmod Connectors
pmod1 = dict({
    "pin_cs"            : Pin.cpu.A4,
    "pin_enable"         : Pin.cpu.B0,
    "pin_synch"         : Pin.cpu.C13,
    "pin_ready"        : Pin.cpu.C5,
    "pin_fault"         : Pin.cpu.C6,
    "spi" : 1
    })

pmod2 = dict({
    "pin_cs"            : Pin.cpu.B12,
    "pin_enable"         : Pin.cpu.C4, 
    "pin_synch"         : Pin.cpu.C7,
    "pin_ready"        : Pin.cpu.C3,
    "pin_fault"         : Pin.cpu.C2,
    "spi" : 2
    })

connector = pmod1
print("Initializing MAX14916PMB...")
max14916pmb = MAX14916PMB(**connector)
#Read and print Rev ID & Status (binary strings)
#TODO

#Set fault and status LED control to autonomous mode
max14916pmb.SLED_control(0)
max14916pmb.FLED_control(0)

print("Enable channels 1-4")
for i in range(1,5):
    max14916pmb.set_HSS(i)
    time.sleep(1)

print("Turn on Open-Wire detection for channel 1 and 2")
#Turn on open-wire detect
max14916pmb.enable_OW_OFF_fault(1)
max14916pmb.enable_OW_OFF_fault(2)
max14916pmb.enable_OW_ON_fault(1)
max14916pmb.enable_OW_ON_fault(2)

print("Wait 4 seconds...")
time.sleep(4)

print ("Open-Wire Detection Results: ",max14916pmb.read_OW_ON_fault())

#Turn off open-wire detect
max14916pmb.disable_OW_OFF_fault(1)
max14916pmb.disable_OW_OFF_fault(2)
max14916pmb.disable_OW_ON_fault(1)
max14916pmb.disable_OW_ON_fault(2)

print("Disable channels 1-4")
for i in range(1,5):
    max14916pmb.clear_HSS(i)
    time.sleep(1)