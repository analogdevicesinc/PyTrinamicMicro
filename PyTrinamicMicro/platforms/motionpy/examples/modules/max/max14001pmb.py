'''
Example using the MAX14001PMB

Created on 27.01.2020

@author: JH
'''

from PyTrinamicMicro.platforms.motionpy.modules.max.max14001 import MAX14001PMB
from pyb import Pin
import time
import logging

# Prepare Logger
logger = logging.getLogger(__name__)
logger.info("Reading ADC values")
csVoltage = Pin.cpu.C0
csCurrent = Pin.cpu.A4

max14001pmb = MAX14001PMB(csVoltage , csCurrent)
filtered = True

while(True):
    currU = max14001pmb.getVoltage(filtered)
    currI = max14001pmb.getCurrent(filtered)
    logger.info("U=" +str(currU)+"V"+" I:" +str(currI)+"A")
    time.sleep(0.5)

