'''
MicroPython main file.
Place as main.py at the root of the Flash memory.

Created on 12.10.2020

@author: LK
'''

# Imports
from PyTrinamicMicro import PyTrinamicMicro as PTM

# Initialize main configuration
PTM.init()

# Execute example script
exec(PTM.script("null"))
