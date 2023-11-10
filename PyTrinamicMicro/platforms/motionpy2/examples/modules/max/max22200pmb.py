################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

"""
Example using the MAX22200PMB#
Created on 2022.10.04
@author: ET
"""

# Paste into terminal to run: exec(open("PyTrinamicMicro/platforms/motionpy2/examples/modules/max/max22200pmb.py").read())

import time
from pyb import Pin
from PyTrinamicMicro.platforms.motionpy2.modules.max.max22200 import MAX22200, MAX22200PMB

pmod1 = dict({
    "pin_cs"        : Pin.cpu.A4,
    "pin_fault"     : Pin.cpu.B0,
    "pin_command"   : Pin.cpu.C6,
    "pin_enable"    : Pin.cpu.C13,
    "pin_trig"      : Pin.cpu.C5,
    "spi" : 1
    })

pmod2 = dict({ # need to test this mapping when boards arrive
    "pin_cs"        : Pin.cpu.B12,
    "pin_fault"     : Pin.cpu.C4,
    "pin_command"   : Pin.cpu.C2,
    "pin_enable"    : Pin.cpu.C7,
    "pin_trig"      : Pin.cpu.C3,
    "spi" : 2
    })

"""Change pmod connector here"""
connector = pmod1
max22200pmb = MAX22200PMB(**connector)

"""Device Setup"""
print("Read Status Register")
max22200pmb.status_reg_flags() # Read fault flags in status register, should read 0x02

print("\nDevice Setup")
# max22200pmb.status_reg(M_OVT, M_OCP, M_OLF, M_HHF, M_DPM, M_COM, M_UVM, FREQM, ch7_6, ch5_4, ch3_2, ch1_0, active)
max22200pmb.status_reg(0, 0, 0, 0, 0, 0, 0, "100kHz", "half", "half", "half", "half", 1)

"""Configure Channels"""
# Copy and paste the following line for each channel that needs to be configured:
# max22200pmb.config_reg(channel, HFS, HOLD_current, TRGnSPI, HIT_current, HIT_time, VDRnCDR, HSnLS, FREQ_CFG, SRC, OL_EN, DPM_EN, HHF_EN)

print("\nChannel Configuration")
max22200pmb.config_reg(0, 0, 10, 0, 45, 100, 0, 0, 1, 0, 0, 0, 0)
# Channel 0 set to full-scale operation, HOLD input = 10, SPI trigger, HIT input = 45, HIT time input = 100, current-drive
# regulation, low-side drive, chopping freq = main freq, fast mode, disable open-load detection, disable detection of
# plunger movement, disable HIT detection

print("\nRead Status Register")
max22200pmb.status_reg_flags() # Read fault flags, should read 0x03

print("\nRead Status Register Again")
max22200pmb.status_reg_flags() # Read fault flags, should read 0x01

print("\nTurn Channel 0 On")
max22200pmb.channel_on_off_spi(0, 1)

# Can now update certain values on-the-fly, refer to datasheet for more info
# Copy and paste the following commands as necessary in the terminal for each channel

"""Turn Channels On/Off"""
#max22200pmb.channel_on_off_spi(channel, status)
#max22200pmb.channel_on_off_trig(status)

"""Adjust HFS and HOLD Current"""
#max22200pmb.HFS_HOLD(channel, HFS, HOLD)

"""Channel Configuration"""
#max22200pmb.channel_config(channel, HFS, HOLD_current, TRGnSPI, HIT_current, HIT_time, VDRnCDR, HSnLS, FREQ_CFG, SRC, OL_EN, DPM_EN, HHF_EN)


# Additional functions for diagnostic purposes:

"""Read Output Channel Register"""
#max22200pmb.read_output(channel) # Return contents of register for selected output

"""Fault Register"""
#max22200pmb.read_faults() # Return all seven channels' faults as 0/1 string (CH0 is LSB)

"""DPM Register"""
#max22200pmb.CFG_DPM(DPM_ISTART, DPM_TDEB, DPM_ITPH, HFS, FREQM, FREQ_CFG) # Set parameters for detection of plunger movement, only available in CDR mode
# HFS/FREQM/FREQ_CFG bits only used for calculations, does not actually set bits
