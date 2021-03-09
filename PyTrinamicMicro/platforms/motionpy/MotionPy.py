'''
MotionPy root configuration class.

Created on 29.10.2020

@author: LK
'''

from PyTrinamicMicro import PyTrinamicMicro
import pyb

class MotionPy(PyTrinamicMicro):

    _MAP_SCRIPT = {
        "null": "PyTrinamicMicro/platforms/motionpy/examples/null.py",
        "linear_distance": "PyTrinamicMicro/platforms/motionpy/examples/linear_distance/linear_distance.py",
        "linear_distance_bounds": "PyTrinamicMicro/platforms/motionpy/examples/linear_distance/linear_distance_bounds.py",
        "blinky": "PyTrinamicMicro/platforms/motionpy/examples/io/blinky.py",
        "buttons_leds": "PyTrinamicMicro/platforms/motionpy/examples/io/buttons_leds.py",
        "hc_sr04_multi_log": "PyTrinamicMicro/platforms/motionpy/examples/modules/hc_sr04_multi/hc_sr04_multi_log.py",
        "tmcm1161_rs232_rotate": "PyTrinamicMicro/platforms/motionpy/examples/modules/TMCM1161/TMCM1161_RS232_rotate.py",
        "tmcm1161_rs485_rotate": "PyTrinamicMicro/platforms/motionpy/examples/modules/TMCM1161/TMCM1161_RS485_rotate.py",
        "tmcm1240_can_rotate": "PyTrinamicMicro/platforms/motionpy/examples/modules/TMCM1240/TMCM1240_CAN_rotate.py",
        "tmcm1240_rs485_rotate": "PyTrinamicMicro/platforms/motionpy/examples/modules/TMCM1240/TMCM1240_RS485_rotate.py",
        "tmcm1270_rotate": "PyTrinamicMicro/platforms/motionpy/examples/modules/TMCM1270/TMCM1270_rotate.py",
        "tmcl_bridge_uart_can": "PyTrinamicMicro/platforms/motionpy/examples/tmcl_bridge/tmcl_bridge_uart_can.py",
        "tmcl_bridge_uart_rs232": "PyTrinamicMicro/platforms/motionpy/examples/tmcl_bridge/tmcl_bridge_uart_rs232.py",
        "tmcl_bridge_uart_rs485": "PyTrinamicMicro/platforms/motionpy/examples/tmcl_bridge/tmcl_bridge_uart_rs485.py",
        "tmcl_bridge_usb_can": "PyTrinamicMicro/platforms/motionpy/examples/tmcl_bridge/tmcl_bridge_usb_can.py",
        "tmcl_bridge_usb_rs232": "PyTrinamicMicro/platforms/motionpy/examples/tmcl_bridge/tmcl_bridge_usb_rs232.py",
        "tmcl_bridge_usb_rs485": "PyTrinamicMicro/platforms/motionpy/examples/tmcl_bridge/tmcl_bridge_usb_rs485.py",
        "tmcl_bridge_usb_uart": "PyTrinamicMicro/platforms/motionpy/examples/tmcl_bridge/tmcl_bridge_usb_uart.py",
        "tmcl_bridge_usb_x": "PyTrinamicMicro/platforms/motionpy/examples/tmcl_bridge/tmcl_bridge_usb_x.py",
        "tmcl_bridge_uart_x": "PyTrinamicMicro/platforms/motionpy/examples/tmcl_bridge/tmcl_bridge_uart_x.py",
        "tmcl_slave_uart": "PyTrinamicMicro/platforms/motionpy/examples/tmcl_bridge/tmcl_slave_uart.py",
        "tmcl_slave_usb": "PyTrinamicMicro/platforms/motionpy/examples/tmcl_bridge/tmcl_slave_usb.py",
        "tmcl_slave_motionpy": "PyTrinamicMicro/platforms/motionpy/examples/tmcl_slave/tmcl_slave_motionpy.py",
        "fw_update_can": "PyTrinamicMicro/platforms/motionpy/examples/firmware_update/fw_update_can.py",
        "can_logger": "PyTrinamicMicro/platforms/motionpy/examples/tmcl_analyzer/can_logger.py",
        "max14001pmb" : "PyTrinamicMicro/platforms/motionpy/examples/modules/max/max14001pmb.py",
        "max14912pmb" : "PyTrinamicMicro/platforms/motionpy/examples/modules/max/max14912pmb.py",
        "max22190pmb" : "PyTrinamicMicro/platforms/motionpy/examples/modules/max/max22190pmb.py"
    }

    _MAP_TEST = {
        "can_version": "PyTrinamicMicro/platforms/motionpy/tests/interfaces/can_version.py",
        "rs232_version": "PyTrinamicMicro/platforms/motionpy/tests/interfaces/rs232_version.py",
        "rs485_version": "PyTrinamicMicro/platforms/motionpy/tests/interfaces/rs485_version.py",
        "version": "PyTrinamicMicro/platforms/motionpy/tests/interfaces/version.py"
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
