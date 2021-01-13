'''
Rotate the motor with TMCM1161 using RS485 interface.

Created on 05.10.2020

@author: LK
'''

from PyTrinamic.modules.TMCM1161.TMCM_1161 import TMCM_1161
from PyTrinamicMicro.platforms.motionpy.connections.rs485_tmcl_interface import rs485_tmcl_interface
import time

con = rs485_tmcl_interface()
module = TMCM_1161(con)

module.rotate(0, 1000)
time.sleep(5)
module.stop(0)

con.close()
