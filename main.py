'''
MicroPython main file.
Place as main.py at the root of the Flash memory.

Created on 12.10.2020

@author: LK
'''

# Imports
from PyTrinamicMicro import PyTrinamicMicro

# Initialize main configuration
PyTrinamicMicro.init()

# Execute example script
exec(open("PyTrinamicMicro/examples/null.py").read())
