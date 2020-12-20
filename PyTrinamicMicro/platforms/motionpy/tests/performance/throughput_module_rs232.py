'''
Test TMCL throughput via RS232 interface and module ID 1.

Created on 19.12.2020

@author: LK
'''

from PyTrinamicMicro.platforms.motionpy.connections.rs232_tmcl_interface import rs232_tmcl_interface
from PyTrinamic.TMCL import TMCL_Request, TMCL_Reply
from pyb import Timer
import pyb
import logging
import math

HOST_ID = 2
MODULE_ID = 1
N_SAMPLES = 50
PAYLOAD = 8
WORST_CASE_LATENCY = 50 # ms

tout = False

def timeout(t):
    global tout
    t.deinit()
    tout = True

def real(ticks, prescaler, freq):
    return ((ticks * freq) / (prescaler + 1))

results = []
timer = Timer(2)

logger = logging.getLogger(__name__)
logger.info("Latency test RS232")

logger.info("Initializing interface.")
interface = rs232_tmcl_interface()

logger.info("Performing test.")
ticks = (WORST_CASE_LATENCY * PAYLOAD * pyb.freq()[2] * 2) / 1000
prescaler = int(ticks / 0x3fffffff)
period = int((WORST_CASE_LATENCY * PAYLOAD * pyb.freq()[2] * 2) / (1000 * (prescaler + 1)))
while(len(results) < N_SAMPLES):
    timer.counter(0)
    timer.init(prescaler=prescaler, period=period, callback=timeout)
    for i in range(0, PAYLOAD):
        interface.send_request_only(TMCL_Request(MODULE_ID, 1, 2, 3, 4, 5), host_id=HOST_ID, module_id=MODULE_ID)
    try:
        for i in range(0, PAYLOAD):
            interface.receive_reply(module_id=MODULE_ID, host_id=HOST_ID)
    except:
        pass
    timer.deinit()
    if(not(tout)):
        counter = timer.counter()
        logger.debug("Measured delta ticks: {}".format(counter))
        results.append((2 * PAYLOAD) / counter)
    else:
        logger.debug("Timeout, not counting")
    tout = False

logger.info("Calculating statistical values.")
min_ticks = min(results)
max_ticks = max(results)
avg_ticks = sum(results) / len(results)
std_dev_ticks = math.sqrt(sum([((i - avg_ticks)**2) for i in results]) / (len(results) - 1))
min_real = real(min_ticks, timer.prescaler(), pyb.freq()[2] * 2) # commands/s
max_real = real(max_ticks, timer.prescaler(), pyb.freq()[2] * 2) # commands/s
avg_real = real(avg_ticks, timer.prescaler(), pyb.freq()[2] * 2) # commands/s
std_dev_real = real(std_dev_ticks, timer.prescaler(), pyb.freq()[2] * 2) # commands/s

logger.info("Minimum: {} commands/tick, Maximum: {} commands/tick, Mean: {} commands/tick, Standard deviation: {} commands/tick".format(min_ticks, max_ticks, avg_ticks, std_dev_ticks))
logger.info("Minimum: {} commands/s, Maximum: {} commands/s, Mean: {} commands/s, Standard deviation: {} commands/s".format(avg_real, std_dev_real))
