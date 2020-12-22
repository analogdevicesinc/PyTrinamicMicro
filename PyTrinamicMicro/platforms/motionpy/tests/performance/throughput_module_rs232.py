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
DATA_RATE = 115200
N_SAMPLES = 10000
PAYLOAD = 1
WORST_CASE_LATENCY = 50 # ms

tout = False

def timeout(t):
    global tout
    t.deinit()
    tout = True

def real(ticks, prescaler, freq):
    return ((ticks * freq) / (prescaler + 1))

min_ticks = 0
max_ticks = 0
avg_ticks = 0
std_dev_ticks = 0
n = 0
timer = Timer(2)

logger = logging.getLogger(__name__)
logger.info("Latency test RS232")

logger.info("Initializing interface.")
interface = rs232_tmcl_interface(data_rate=DATA_RATE)

logger.info("Performing test.")
ticks = (WORST_CASE_LATENCY * PAYLOAD * pyb.freq()[2] * 2) / 1000
prescaler = int(ticks / 0x3fffffff)
period = int((WORST_CASE_LATENCY * PAYLOAD * pyb.freq()[2] * 2) / (1000 * (prescaler + 1)))
while(n < N_SAMPLES):
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
        # update values
        value = (2 * PAYLOAD) / counter
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
    else:
        logger.debug("Timeout, not counting")
    tout = False

logger.info("Calculating statistical values.")
std_dev_ticks = math.sqrt(std_dev_ticks)
min_real = real(min_ticks, timer.prescaler(), pyb.freq()[2] * 2) # commands/s
max_real = real(max_ticks, timer.prescaler(), pyb.freq()[2] * 2) # commands/s
avg_real = real(avg_ticks, timer.prescaler(), pyb.freq()[2] * 2) # commands/s
std_dev_real = real(std_dev_ticks, timer.prescaler(), pyb.freq()[2] * 2) # commands/s

logger.info("Minimum: {} commands/tick, Maximum: {} commands/tick, Mean: {} commands/tick, Standard deviation: {} commands/tick".format(min_ticks, max_ticks, avg_ticks, std_dev_ticks))
logger.info("Minimum: {} commands/s, Maximum: {} commands/s, Mean: {} commands/s, Standard deviation: {} commands/s".format(min_real, max_real, avg_real, std_dev_real))
