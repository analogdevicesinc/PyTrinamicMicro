'''
Control the LEDs with the buttons.

Created on 14.10.2020

@author: LK
'''

from pyb import Pin
import logging

# Define button list for all buttons on board
buttons = [
    ("S1", Pin(Pin.cpu.C3, Pin.IN, pull=Pin.PULL_UP)),
    ("S2", Pin(Pin.cpu.C2, Pin.IN, pull=Pin.PULL_UP))
]

# Define default button states
button_states = {
    buttons[0][0]: 1,
    buttons[1][0]: 1
}

# Define dict to map button to control LED
leds = {
    buttons[0][0]: ("LEDG2", Pin(Pin.cpu.A15, Pin.OUT_PP), False),
    buttons[1][0]: ("LEDR2", Pin(Pin.cpu.B4, Pin.OUT_PP), False)
}

# Prepare Logger
logger = logging.getLogger(__name__)
logger.info("Blinky for all LEDs on board")

# Set initial state
logger.info("Setting initial state ...")
for led in leds.values():
    led[1].value(led[2])
logger.info("Initial state set.")

while(True):
    for button in buttons:
        val = button[1].value()
        led = leds[button[0]]
        if((val == 0) and (button_states[button[0]] == 1)):
            logger.info("Button {} pressed.".format(button[0]))
            led[1].value(not(led[1].value()))
            logger.debug("New {} state: {}".format(led[0], led[1].value()))
        if((val == 1) and (button_states[button[0]] == 0)):
            logger.info("Button {} released.".format(button[0]))
        button_states[button[0]] = val
