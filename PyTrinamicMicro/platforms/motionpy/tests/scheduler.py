'''
Test the scheduler.

Created on 15.12.2020

@author: LK
'''

from PyTrinamicMicro.platforms.motionpy.Scheduler import Scheduler
from pyb import RTC
import logging

TICK_INTERVAL = 1000 # ms

logger = logging.getLogger(__name__)
res_a = 0
res_b = 0
res_c = 0
res_d = 0

def single(a, b):
    global res_a, res_b
    res_a = a
    res_b = b

def periodic(c, d):
    global res_c, res_d
    res_c += c
    res_d += d

logger.info("Test scheduler")

logger.info("Initializing scheduler.")
sched = Scheduler(interval=TICK_INTERVAL)

logger.info("Registering tasks.")
now = RTC().datetime()
sched.register_task(0, sched.add_dates(now, (0, 0, 0, 0, 0, 0, 10)),
    None, single, 1, b=2)
sched.register_task(1, sched.add_dates(now, (0, 0, 0, 0, 0, 0, 10)),
    (0, 0, 0, 0, 0, 0, 10), periodic, 3, d=4)

logger.info("Starting scheduler.")
sched.start()

logger.info("Now: {}, Now + 22s: {}".format(now, sched.add_dates(now, (0, 0, 0, 0, 0, 0, 22))))

logger.info("Waiting for results to change.")
while(not(sched.due(sched.add_dates(now, (0, 0, 0, 0, 0, 0, 12)), RTC().datetime()))):
    #print("{}, {}, {}, {}".format(res_a, res_b, res_c, res_d))
    if((res_a == 1) and (res_b == 2) and (res_c == 3) and (res_d == 4)):
        break
else:
    assert False, "Function not called on due."
logger.info("Single results changed.")

while(not(sched.due(sched.add_dates(now, (0, 0, 0, 0, 0, 0, 22)), RTC().datetime()))):
    if((res_c == 6) and (res_d == 8)):
        break
else:
    assert False, "Periodic function not called periodically."
logger.info("Periodic results changed.")

logger.info("Stopping scheduler.")
sched.stop()

logger.info("Test completed successfully.")
