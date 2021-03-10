'''
Example using the MAX14914PMB.
This scripts displays the readout of the max14914 in digital input mode.
Created on 5.03.2021

@author: JH
'''
from pyb import Pin 
from PyTrinamicMicro.platforms.motionpy.modules.max.max14914 import MAX14914
import time
import logging

logger = logging.getLogger(__name__)
logger.info("MAX14914PMB Input example running")

module = MAX14914()

module.setIOMode(1)

description = """\nThis scripts displays the readout of the max14914 in digital input mode.\n """
print(description)
while(True):
    for cursor in '|/-\\':
        state = module.getDIDO_LVL()
        faults = module.getFault()
        OV_VDD = module.getOV_VDD()
        text =  cursor+" Input state: " +  str(state) + ";Fault state: " + str(faults) +"; OV_VDD: " + str(OV_VDD)
        print(text, end='\r')
        time.sleep(0.1)
4