'''
Example using the MAX14914PMB.
This scripts toggles output of MAX14914.
Created on 5.03.2021

@author: JH
'''
from pyb import Pin
from PyTrinamicMicro.platforms.motionpy.modules.max.max14914 import MAX14914
import time
import logging

logger = logging.getLogger(__name__)
logger.info("MAX14914PMB Output example running")

module = MAX14914()
module.setIOMode(0)

description = """\nThis scripts toggles output of MAX14914.\n """
print(description)
while(True):
        state = 0
        module.setDO(state)
        faults = module.getFault()
        OV_VDD = module.getOV_VDD()
        for cursor in '|/-\\':
                text =  cursor+" Output state: " +  str(state) + ";Fault state: " + str(faults) +"; OV_VDD: " + str(OV_VDD)
                print(text, end='\r')        
                time.sleep(0.2)
        state = 1
        module.setDO(state)
        faults = module.getFault()
        OV_VDD = module.getOV_VDD()
        for cursor in '|/-\\':
                text =  cursor+" Output state: " +  str(state) + ";Fault state: " + str(faults) +"; OV_VDD: " + str(OV_VDD)
                print(text, end='\r')
                time.sleep(0.2)
        