'''
Test TMCL latency via CAN interface and module ID 1.

Created on 19.12.2020

@author: LK
'''

from PyTrinamicMicro.platforms.motionpy.connections.can_tmcl_interface import can_tmcl_interface
from PyTrinamic.TMCL import TMCL_Request, TMCL_Reply
from pyb import Timer
import pyb
import logging
import math

HOST_ID = 2
MODULE_ID = 1
N_SAMPLES = 10000

tout = False

def timeout(t):
    global tout
    t.deinit()
    tout = True

def real(ticks, prescaler, freq):
    return ((ticks * (prescaler + 1)) / freq)

min_ticks = 0
max_ticks = 0
avg_ticks = 0
std_dev_ticks = 0
n = 0
timer = Timer(2)

logger = logging.getLogger(__name__)
logger.info("Latency test CAN")

logger.info("Initializing interface.")
interface = can_tmcl_interface()

logger.info("Performing test.")
while(n < N_SAMPLES):
    timer.counter(0)
    timer.init(prescaler=0, period=16800000, callback=timeout)
    # send invalid (for all modules) TMCL Request
    reply = interface.send_request(TMCL_Request(MODULE_ID, 1, 2, 3, 4, 5), host_id=HOST_ID, module_id=MODULE_ID)
    timer.deinit()
    if(not(tout)):
        counter = timer.counter()
        logger.debug("Measured delta ticks: {}".format(counter))
        # update values
        value = counter
        if(n == 0):
            min_ticks = value
            max_ticks = value
            avg_ticks = value
            std_dev_ticks = 0
        else:
            min_ticks = min(min_ticks, value)
            max_ticks = max(max_ticks, value)
            avg_ticks_new = avg_ticks + ((value - avg_ticks) / (n + 1))
            std_dev_ticks = (((n - 1) * std_dev_ticks) + ((value - avg_ticks_new) * (value - avg_ticks))) / n
            avg_ticks = avg_ticks_new
        n += 1
    tout = False

logger.info("Calculating statistical values.")
std_dev_ticks = math.sqrt(std_dev_ticks)
min_real = real(min_ticks, timer.prescaler(), pyb.freq()[2] * 2) * 1000 # ms
max_real = real(max_ticks, timer.prescaler(), pyb.freq()[2] * 2) * 1000 # ms
avg_real = real(avg_ticks, timer.prescaler(), pyb.freq()[2] * 2) * 1000 # ms
std_dev_real = real(std_dev_ticks, timer.prescaler(), pyb.freq()[2] * 2) * 1000 # ms

logger.info("Minimum: {} ticks, Maximum: {} ticks, Mean: {} ticks, Standard deviation: {} ticks".format(min_ticks, max_ticks, avg_ticks, std_dev_ticks))
logger.info("Minimum: {} ms, Maximum: {} ms, Mean: {} ms, Standard deviation: {} ms".format(min_real, max_real, avg_real, std_dev_real))
