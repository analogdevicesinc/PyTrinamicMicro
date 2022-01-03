'''
Example using the MAX22007PMB

Created on 13.10.2021

@author: 
'''
##############################################################################
import time
from pyb import Pin
from  PyTrinamicMicro.platforms.motionpy2.modules.max import max22007

#For readability
SECONDS = 1

#Pmod Connectors
pmod0 = dict({
    "pin_intb"  : Pin.cpu.C6,
    "pin_cs"    : Pin.cpu.A4,
    "spi" : 1
    })

pmod1 = dict({
    "pin_intb"  : Pin.cpu.C2,
    "pin_cs"    : Pin.cpu.B12, 
    "spi" : 2
    })

connector = pmod0
print("Initializing MAX22007PMB...")
max22007pmb = max22007.MAX22007PMB(**connector)

#Read and print Rev ID & Status (binary strings)
temp = max22007pmb.dac.read(max22007pmb.dac.MAX22007_REV_adr)
print("MAX22007 Rev#:" + str(temp))

temp = max22007pmb.dac.read(max22007pmb.dac.MAX22007_STAT_adr)
print("MAX22007 Status:" + str(temp))

#Toggle LEDs and set to 5 V for each channel. 
channels_on = [0,0,0,0]
while(True):
    for i in (1,2,3,4):
        if (channels_on[i-1] == 0):
            data = max22007pmb.set_LED(i)
            data = max22007pmb.set_channel_voltage(i, 5.0)
            channels_on[i-1] = 1
        else:
            data = max22007pmb.clear_LED(i)
            data = max22007pmb.set_channel_voltage(i, 0.0)
            channels_on[i-1] = 0
        time.sleep(0.5*SECONDS)