'''
Update firmware of attached board via CAN.
Firmware .hex file must be stored as "firmware.hex" in the path.

Created on 19.10.2020

@author: LK
'''

from PyTrinamicMicro.connections.can_tmcl_interface import can_tmcl_interface
from PyTrinamicMicro.tmcl_bootloader import *
import logging
import time

MODULE_ID = 1

con = can_tmcl_interface()
con.sendBoot()
time.sleep(3.0)
boot = tmcl_bootloader(con, MODULE_ID)
boot.update_firmware(open("firmware.hex", "rt"), True)
