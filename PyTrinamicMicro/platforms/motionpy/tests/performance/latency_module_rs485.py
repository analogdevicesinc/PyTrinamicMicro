'''
Test TMCL latency via RS485 interface and module ID 1.

Created on 19.12.2020

@author: LK
'''

from PyTrinamicMicro.platforms.motionpy.connections.rs485_tmcl_interface import rs485_tmcl_interface
from PyTrinamic.TMCL import TMCL_Request, TMCL_Reply
from pyb import Timer
import logging
import math

HOST_ID = 2
MODULE_ID = 1
N_SAMPLES = 1000

tout = False

def timeout(t):
    global counter
    t.deinit()
    tout = True

results = []
timer = Timer(2)

logger = logging.getLogger(__name__)
logger.info("Latency test RS485")

logger.info("Initializing interface.")
interface = rs485_tmcl_interface()

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
avg = sum(results) / len(results)
std_dev = math.sqrt(sum([((i - avg)**2) for i in results]) / (len(results) - 1))
avg_real = (avg * 0.2) / 16800 # ms
std_dev_real = (std_dev * 0.2) / 16800 # ms

logger.info("Mean: {} ticks, Standard deviation: {} ticks".format(avg, std_dev))
logger.info("Mean: {} ms, Standard deviation: {} ms".format(avg_real, std_dev_real))
