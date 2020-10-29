'''
MicroPython main file.
Place as main.py at the root of the Flash memory.

Created on 12.10.2020

@author: LK
'''

# Imports
from PyTrinamicMicro.platforms.motionpy.MotionPy import MotionPy as MP

# Initialize main configuration
MP.init()

# Execute example script
exec(MP.script("null"))
