################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
Example using the MAX14912PMB.
This script switches all the outputs to high and then back to low. 
Created on 15.02.2021

@author: JH
'''
from pyb import Pin
from PyTrinamicMicro.platforms.motionpy2.modules.max.max14912 import MAX14912
import time
import logging

logger = logging.getLogger(__name__)
logger.info("MAX14912PMB example running")

pmod0 = dict({
    "pin_cs"    :   Pin.cpu.A4,
    "pin_fltr"  :   Pin.cpu.C6, 
    "pin_cmd"   :   Pin.cpu.C13,
    "spi"       :   1,
    })


pmod1 = dict({
    "pin_cs"    :   Pin.cpu.B12,
    "pin_fltr"  :   Pin.cpu.C2, 
    "pin_cmd"   :   Pin.cpu.C7,
    "spi"       :   2,
    })

'''Change pmod connector here'''
connector = pmod0

max14912 = MAX14912(connector["pin_cs"],connector["spi"],connector["pin_fltr"],connector["pin_cmd"] )

while(True):
    logger.info("Switching everything to HIGH")
    for y in range(0, 8):
        max14912.set_output(y,1)
        time.sleep(0.25)
    logger.info("Switching everything to LOW")
    for y in range(0, 8):
        max14912.set_output(y,0)
        time.sleep(0.25)
