'''
MicroPython main file.
Place as main.py at the root of the Flash memory.

Created on 12.10.2020

@author: LK
'''

# Imports
from PyTrinamicMicro.platforms.motionpy2.MotionPy import MotionPy as MP

# Initialize main configuration
MP.init()

def test_master():
    exec(open("PyTrinamicMicro/platforms/motionpy2/tests/interfaces/version.py").read())

def test_slave():
    exec(open("PyTrinamicMicro/platforms/motionpy2/examples/tmcl_slave/tmcl_slave_all.py").read())
