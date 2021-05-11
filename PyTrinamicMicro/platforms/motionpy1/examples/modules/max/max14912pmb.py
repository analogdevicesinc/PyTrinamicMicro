'''
Example using the MAX14912PMB.
This script switches all the outputs to high and then back to low.
Created on 15.02.2021

@author: JH
'''
from pyb import Pin
from PyTrinamicMicro.platforms.motionpy1.modules.max.max14912 import MAX14912
import time
import logging

logger = logging.getLogger(__name__)
logger.info("MAX14912PMB example running")

pins = dict({
    "pin_cs"    :   Pin.cpu.C0,
    "spi"       :   1,
    "pin_fltr"  :   Pin.cpu.A4,
    "pin_cmd"   :   Pin.cpu.C1,
    })

module = MAX14912(pins["pin_cs"],pins["spi"],pins["pin_fltr"],pins["pin_cmd"] )

while(True):
    logger.info("Switching everything to HIGH")
    for y in range(0, 8):
        module.set_output(y,1)
        time.sleep(0.25)
    logger.info("Switching everything to LOW")
    for y in range(0, 8):
        module.set_output(y,0)
        time.sleep(0.25)
