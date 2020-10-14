'''
Blink the LEDs.

Created on 14.10.2020

@author: LK
'''

from pyb import Pin
import time
import logging

# Prepare Logger
logger = logging.getLogger(__name__)
logger.info("Blinky for all LEDs on board")

# Define LED list for all LEDs on board
leds = [
    ("LEDG1", Pin(Pin.cpu.A13, Pin.OUT_PP), True),
    ("LEDR1", Pin(Pin.cpu.A14, Pin.OUT_PP), False),
    ("LEDG2", Pin(Pin.cpu.A15, Pin.OUT_PP), True),
    ("LEDR2", Pin(Pin.cpu.B4, Pin.OUT_PP), False)
]

# Set initial state
logger.info("Setting initial state ...")
for led in leds:
    led[1].value(led[2])
logger.info("Initial state set.")

# Blink all LEDs
while(True):
    logger.debug("Blinking LEDs.")
    for led in leds:
        led[1].value(not(led[1].value()))
        logger.debug("New {} state: {}".format(led[0], led[1].value()))
    time.sleep(0.5)
