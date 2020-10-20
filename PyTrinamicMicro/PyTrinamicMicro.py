'''
PyTrinamicMicro root class, used for settings etc.

Created on 13.10.2020

@author: LK
'''

import logging


class PyTrinamicMicro(object):

    # Public constants
    LOGGING_VERBOSITY = logging.DEBUG
    LOGGING_FILE_NAME = "{}.log".format(__module__)
    LOGGING_CONSOLE_ENABLED = True
    LOGGING_FILE_ENABLED = False

    # Public variables
    logging_console_enabled = LOGGING_CONSOLE_ENABLED
    logging_file_enabled = LOGGING_FILE_ENABLED

    # Private constants
    __MAP_SCRIPT = {
        "null": "PyTrinamicMicro/examples/null.py",
        "blinky": "PyTrinamicMicro/examples/io/blinky.py",
        "buttons_leds": "PyTrinamicMicro/examples/io/buttons_leds.py",
        "tmcm1161_rs232_rotate": "PyTrinamicMicro/examples/modules/TMCM1161/TMCM1161_RS232_rotate.py",
        "tmcm1161_rs485_rotate": "PyTrinamicMicro/examples/modules/TMCM1161/TMCM1161_RS485_rotate.py",
        "tmcm1270_rotate": "PyTrinamicMicro/examples/modules/TMCM1270/TMCM1270_rotate.py",
        "tmcl_bridge_uart_can": "PyTrinamicMicro/examples/tmcl_bridge/tmcl_bridge_uart_can.py",
        "tmcl_bridge_uart_rs232": "PyTrinamicMicro/examples/tmcl_bridge/tmcl_bridge_uart_rs232.py",
        "tmcl_bridge_uart_rs485": "PyTrinamicMicro/examples/tmcl_bridge/tmcl_bridge_uart_rs485.py",
        "tmcl_bridge_usb_can": "PyTrinamicMicro/examples/tmcl_bridge/tmcl_bridge_usb_can.py",
        "tmcl_bridge_usb_rs232": "PyTrinamicMicro/examples/tmcl_bridge/tmcl_bridge_usb_rs232.py",
        "tmcl_bridge_usb_rs485": "PyTrinamicMicro/examples/tmcl_bridge/tmcl_bridge_usb_rs485.py",
        "tmcl_bridge_usb_uart": "PyTrinamicMicro/examples/tmcl_bridge/tmcl_bridge_usb_uart.py",
        "tmcl_slave_uart": "PyTrinamicMicro/examples/tmcl_bridge/tmcl_slave_uart.py",
        "tmcl_slave_usb": "PyTrinamicMicro/examples/tmcl_bridge/tmcl_slave_usb.py",
        "fw_update_can": "PyTrinamicMicro/examples/firmware_update/fw_update_can.py"
    }

    # Private variables
    __logger = None
    __console_handler = None
    __file_handler = None

    @staticmethod
    def init():
        PyTrinamicMicro.__init_logger()
        PyTrinamicMicro.__logger.debug("Root logger initialized.")
        PyTrinamicMicro.__logger.debug("PyTrinamicMicro initialized.")

    @staticmethod
    def script(identifier):
        return compile(open(PyTrinamicMicro.__MAP_SCRIPT.get(identifier.lower())).read(), "<string>", "exec")

    @staticmethod
    def set_logging_console_enabled(enabled):
        if(enabled and not(PyTrinamicMicro.logging_console_enabled)):
            PyTrinamicMicro.__logger.addHandler(PyTrinamicMicro.__console_handler)
        elif(not(enabled) and PyTrinamicMicro.logging_console_enabled):
            PyTrinamicMicro.__logger.removeHandler(PyTrinamicMicro.__console_handler)
        PyTrinamicMicro.logging_console_enabled = enabled

    @staticmethod
    def set_logging_file_enabled(enabled):
        if(enabled and not(PyTrinamicMicro.logging_file_enabled)):
            PyTrinamicMicro.__logger.addHandler(PyTrinamicMicro.__file_handler)
        elif(not(enabled) and PyTrinamicMicro.logging_file_enabled):
            PyTrinamicMicro.__logger.removeHandler(PyTrinamicMicro.__file_handler)
        PyTrinamicMicro.logging_file_enabled = enabled

    @staticmethod
    def set_logging_enabled(enabled):
        PyTrinamicMicro.set_logging_console_enabled(enabled)
        PyTrinamicMicro.set_logging_file_enabled(enabled)

    @staticmethod
    def __init_logger():
        PyTrinamicMicro.__logger = logging.getLogger()
        formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
        PyTrinamicMicro.__logger.setLevel(PyTrinamicMicro.LOGGING_VERBOSITY)

        PyTrinamicMicro.__console_handler = logging.StreamHandler()
        PyTrinamicMicro.__console_handler.setFormatter(formatter)
        if(PyTrinamicMicro.logging_console_enabled):
            PyTrinamicMicro.__logger.addHandler(PyTrinamicMicro.__console_handler)

        PyTrinamicMicro.__file_handler = logging.FileHandler(PyTrinamicMicro.LOGGING_FILE_NAME)
        PyTrinamicMicro.__file_handler.setFormatter(formatter)
        if(PyTrinamicMicro.logging_file_enabled):
            PyTrinamicMicro.__logger.addHandler(PyTrinamicMicro.__file_handler)
