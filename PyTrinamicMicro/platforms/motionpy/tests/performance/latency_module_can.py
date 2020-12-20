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
N_SAMPLES = 1000

tout = False

def timeout(t):
    global tout
    t.deinit()
    tout = True

def real(ticks, prescaler, freq):
    return ((ticks * (prescaler + 1)) / freq)

results = []
timer = Timer(2)

logger = logging.getLogger(__name__)
logger.info("Latency test CAN")

logger.info("Initializing interface.")
interface = can_tmcl_interface()

logger.info("Performing test.")
while(len(results) < N_SAMPLES):
    timer.counter(0)
    timer.init(prescaler=0, period=16800000, callback=timeout)
    # send invalid (for all modules) TMCL Request
    reply = interface.send_request(TMCL_Request(MODULE_ID, 1, 2, 3, 4, 5), host_id=HOST_ID, module_id=MODULE_ID)
    timer.deinit()
    if(not(tout)):
        counter = timer.counter()
        logger.debug("Measured delta ticks: {}".format(counter))
        results.append(counter)
    tout = False

logger.info("Calculating statistical values.")
min_ticks = min(results)
max_ticks = max(results)
avg_ticks = sum(results) / len(results)
std_dev_ticks = math.sqrt(sum([((i - avg_ticks)**2) for i in results]) / (len(results) - 1))
min_real = real(min_ticks, timer.prescaler(), pyb.freq()[2] * 2) * 1000 # ms
max_real = real(max_ticks, timer.prescaler(), pyb.freq()[2] * 2) * 1000 # ms
avg_real = real(avg_ticks, timer.prescaler(), pyb.freq()[2] * 2) * 1000 # ms
std_dev_real = real(std_dev_ticks, timer.prescaler(), pyb.freq()[2] * 2) * 1000 # ms

logger.info("Minimum: {} ticks, Maximum: {} ticks, Mean: {} ticks, Standard deviation: {} ticks".format(min_ticks, max_ticks, avg_ticks, std_dev_ticks))
logger.info("Minimum: {} ms, Maximum: {} ms, Mean: {} ms, Standard deviation: {} ms".format(min_real, max_real, avg_real, std_dev_real))
