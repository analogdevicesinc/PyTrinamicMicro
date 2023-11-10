################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

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

DI1     =   Pin(Pin.cpu.C1,Pin.OUT_PP)
DI2     =  Pin(Pin.cpu.A7, Pin.OUT_PP)

while(True):
    for cursor in '|/-\\':
        DI1_lvl = DI1.value()
        DI2_lvl = DI2.value()
        text =  cursor+" DI1 state: " +  str(DI1_lvl) + "; DI2 state: " + str(DI2_lvl)
        print(text, end='\r')
        time.sleep(0.2)
