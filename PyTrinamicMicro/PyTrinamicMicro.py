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
    LOGGING_CONSOLE_ENABLED = False
    LOGGING_FILE_ENABLED = True

    # Public variables
    logging_console_enabled = LOGGING_CONSOLE_ENABLED
    logging_file_enabled = LOGGING_FILE_ENABLED

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
    def enable_logging_console():
        if(not(PyTrinamicMicro.logging_console_enabled)):
            PyTrinamicMicro.__logger.addHandler(PyTrinamicMicro.__console_handler)
        PyTrinamicMicro.logging_console_enabled = True

    @staticmethod
    def disable_logging_console():
        if(PyTrinamicMicro.logging_console_enabled):
            PyTrinamicMicro.__logger.removeHandler(PyTrinamicMicro.__console_handler)
        PyTrinamicMicro.logging_console_enabled = False

    @staticmethod
    def set_logging_console_enabled(enabled):
        if(enabled):
            PyTrinamicMicro.enable_logging_console()
        else:
            PyTrinamicMicro.disable_logging_console()

    @staticmethod
    def enable_logging_file():
        if(not(PyTrinamicMicro.logging_file_enabled)):
            PyTrinamicMicro.__logger.addHandler(PyTrinamicMicro.__file_handler)
        PyTrinamicMicro.logging_file_enabled = True

    @staticmethod
    def disable_logging_file():
        if(PyTrinamicMicro.logging_file_enabled):
            PyTrinamicMicro.__logger.removeHandler(PyTrinamicMicro.__file_handler)
        PyTrinamicMicro.logging_file_enabled = False

    @staticmethod
    def set_logging_file_enabled(enabled):
        if(enabled):
            PyTrinamicMicro.enable_logging_file()
        else:
            PyTrinamicMicro.disable_logging_file()

    @staticmethod
    def enable_logging():
        PyTrinamicMicro.enable_logging_console()
        PyTrinamicMicro.enable_logging_file()

    @staticmethod
    def disable_logging():
        PyTrinamicMicro.disable_logging_console()
        PyTrinamicMicro.disable_logging_file()

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
        PyTrinamicMicro.logging_console_enabled = not(PyTrinamicMicro.logging_console_enabled)
        PyTrinamicMicro.set_logging_console_enabled(not(PyTrinamicMicro.logging_console_enabled))

        PyTrinamicMicro.__file_handler = logging.FileHandler(PyTrinamicMicro.LOGGING_FILE_NAME)
        PyTrinamicMicro.__file_handler.setFormatter(formatter)
        PyTrinamicMicro.logging_file_enabled = not(PyTrinamicMicro.logging_file_enabled)
        PyTrinamicMicro.set_logging_file_enabled(not(PyTrinamicMicro.logging_file_enabled))
