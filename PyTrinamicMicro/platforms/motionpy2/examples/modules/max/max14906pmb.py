################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
Example using the MAX14906PMB#

Created on 13.10.2021

@author: KA
'''
#Paste into terminal to run: exec(open("PyTrinamicMicro/platforms/motionpy2/examples/modules/max/max14906pmb.py").read())

from PyTrinamicMicro.platforms.motionpy2.modules.max.max14906 import MAX14906, MAX14906PMB
from pyb import Pin
import time
import logging

# Prepare Logger
logger = logging.getLogger(__name__)
logger.info("Channel 1: Digital Output    Channel 2: Digital Input")

pmod1 = dict({
    "pin_cs"            : Pin.cpu.A4,
    "pin_ready"         : Pin.cpu.B0,
    "pin_synch"         : Pin.cpu.C13,
    "pin_enable"        : Pin.cpu.C5,
    "pin_fault"         : Pin.cpu.C6,
    "spi" : 1
    })

pmod2 = dict({
    "pin_cs"            : Pin.cpu.B12,
    "pin_ready"         : Pin.cpu.C4, 
    "pin_synch"         : Pin.cpu.C7,
    "pin_enable"        : Pin.cpu.C3,
    "pin_fault"         : Pin.cpu.C2,
    "spi" : 2
    })

'''Change pmod connector here'''
connector = pmod1
max14906pmb = MAX14906PMB(**connector)

#test script to communicate with PMB

channel_DO = 1 #Channel 1 is digital output 
channel_DI = 2 #Channel 2 is digital input

#enable SLED control 
max14906pmb.SLED_control() 
out = 0

#Configure Channel 1 DO:
max14906pmb.set_DO(channel_DO) #enable digital output mode for channel 1
#max14906pmb.high_side_mode(channel_DO) #default
#max14906pmb.high_side_modex2(channel_DO)
#max14906pmb.current_lim_set(channel_DO, "130mA") #600mA, 130mA, 300mA, 1.2A
#max14906pmb.push_pull_mode_active(channel_DO)
#max14906pmb.push_pull_mode_simple(channel_DO)

#Enable desired faults for DO: 
max14906pmb.enable_OW_fault(channel_DO) #only available in DO high side mode
max14906pmb.enable_ShVDD(channel_DO) #only available in DO high side mode
max14906pmb.masking(2, 0) #disable masking for open-wire fault
max14906pmb.masking(4, 0) #disable masking for short-to-VDD fault

#Configure Channel 2 DI:
max14906pmb.set_DI(channel_DI)
#max14906pmb.DI_type(2) #default is type 1/type 3 


period = 5
while(True): 
    for cursor in '|/-\\':
        #toggle channel 1 DO 
        if out == 0:
            channel1_status = max14906pmb.static_high_mode(channel_DO)
            max14906pmb.set_SLED(channel_DO, 1)
        else:
            channel1_status = max14906pmb.static_low_mode(channel_DO)
            max14906pmb.set_SLED(channel_DO, 0)
        out = ~out

        #read channel 2 input
        d_input = max14906pmb.read_DI(channel_DI)

        #read faults
        ow = max14906pmb.read_OW_fault()
        shvdd = max14906pmb.read_ShVDD_fault()
        g_err = max14906pmb.read_global_err()

        text = cursor + " Channel " + str(channel_DO) + ": " +  channel1_status + " Channel " + str(channel_DI) + ": " + d_input + " WDogErr: " + g_err[0] + " LossGND: " + g_err[1] + " ThrmShutd: " + g_err[2] + " VDD_UVLO: " + g_err[3] + " VDD_Warn: " + g_err[4] + " VDD_Low: " + g_err[5] + " V5_UVLO : " + g_err[6] + " VINT_UV: " +g_err[7] + " OpnWrFault: " + ow + " ShtVDDFault: " + shvdd
        print(text, end='\r')
        time.sleep(period/2)


