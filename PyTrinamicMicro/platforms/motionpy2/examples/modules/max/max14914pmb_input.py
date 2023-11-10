################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
Example using the MAX14914PMB.
This scripts displays the readout of the max14914 in digital input mode.
Created on 5.03.2021

@author: JH
'''
from pyb import Pin 
from PyTrinamicMicro.platforms.motionpy2.modules.max.max14914 import MAX14914
import time
import logging

logger = logging.getLogger(__name__)
logger.info("MAX14914PMB Input example running")

pmod0 = dict({
    "do_set_pin"    :   Pin.cpu.A5,
    "do_pp_pin"     :   Pin.cpu.A6,
    "di_ena_pin"    :   Pin.cpu.A7,
    "dido_lvl_pin"  :   Pin.cpu.A4, 
    "fault_pin"     :   Pin.cpu.C6,
    "ov_vdd_pin"    :   Pin.cpu.B0
    })

pmod1 = dict({
    "do_set_pin"    :   Pin.cpu.B13,
    "do_pp_pin"     :   Pin.cpu.B14,
    "di_ena_pin"    :   Pin.cpu.B15,
    "dido_lvl_pin"  :   Pin.cpu.B12, 
    "fault_pin"     :   Pin.cpu.C2,
    "ov_vdd_pin"    :   Pin.cpu.C4
    })

'''Change pmod connector here'''
connector = pmod0
module = MAX14914(connector["do_set_pin"], connector["do_pp_pin"], connector["di_ena_pin"], connector["dido_lvl_pin"], connector["fault_pin"], connector["ov_vdd_pin"])

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
