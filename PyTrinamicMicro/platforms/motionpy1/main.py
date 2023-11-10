################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
MicroPython main file.
Place as main.py at the root of the Flash memory.

Created on 12.10.2020

@author: LK
'''

# Imports
from PyTrinamicMicro.platforms.motionpy1.MotionPy import MotionPy as MP

# Initialize main configuration
MP.init()

# Execute example script
#exec(MP.script("null"))
