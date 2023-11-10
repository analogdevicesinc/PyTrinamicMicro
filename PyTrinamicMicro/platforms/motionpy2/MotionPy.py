################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
MotionPy root configuration class.

Created on 29.10.2020

@author: LK
'''

from PyTrinamicMicro import PyTrinamicMicro
import pyb

class MotionPy(PyTrinamicMicro):

    _MAP_SCRIPT = {
        "tmcl_slave_demo": "PyTrinamicMicro/platforms/motionpy2/examples/tmcl_slave/tmcl_slave_demo.py",
        "tmcl_bridge_usb_can": "PyTrinamicMicro/platforms/motionpy2/examples/tmcl_bridge/tmcl_bridge_usb_can.py",
        "can_logger": "PyTrinamicMicro/platforms/motionpy2/examples/tmcl_analyzer/can_logger.py",
        "blinky": "PyTrinamicMicro/platforms/motionpy2/examples/io/blinky.py"
    }

    _MAP_TEST = {
        "can_version": "PyTrinamicMicro/platforms/motionpy2/tests/interfaces/can_version.py",
        "rs232_version": "PyTrinamicMicro/platforms/motionpy2/tests/interfaces/rs232_version.py",
        "rs485_version": "PyTrinamicMicro/platforms/motionpy2/tests/interfaces/rs485_version.py",
        "version": "PyTrinamicMicro/platforms/motionpy2/tests/interfaces/version.py"
    }

    @staticmethod
    def script(identifier):
        return PyTrinamicMicro.script(MotionPy, identifier)

    @staticmethod
    def test(identifier):
        return PyTrinamicMicro.test(MotionPy, identifier)

    @staticmethod
    def repl_uart():
        pyb.repl_uart(pyb.UART(3, 9600))

    @staticmethod
    def init_time(datetime):
        pyb.RTC().datetime(datetime)
