'''
PyTrinamicMicro root class, used for settings etc.

Created on 13.10.2020

@author: LK
'''

import logging


class PyTrinamicMicro(object):

    # Public constants
    LOGGING_VERBOSITY = logging.DEBUG
    LOGGING_CONSOLE = False
    LOGGING_FILE = True
    LOGGING_FILE_NAME = "{}.log".format(__module__)

    # Public variables
    logging_enabled = True

    # Private variables
    __logger = None
    __logging_handlers = []

    @staticmethod
    def init():
        PyTrinamicMicro.__init_logger()
        PyTrinamicMicro.__logger.debug("Root logger initialized.")
        PyTrinamicMicro.__logger.debug("PyTrinamicMicro initialized.")

    @staticmethod
    def enable_logging():
        if(not(PyTrinamicMicro.logging_enabled)):
            for handler in PyTrinamicMicro.__logging_handlers:
                PyTrinamicMicro.__logger.addHandler(handler)

    @staticmethod
    def disable_logging():
        if(PyTrinamicMicro.logging_enabled):
            for handler in PyTrinamicMicro.__logging_handlers:
                PyTrinamicMicro.__logger.removeHandler(handler)

    @staticmethod
    def set_logging_enabled(enabled):
        if(enabled):
            PyTrinamicMicro.enable_logging()
        else:
            PyTrinamicMicro.disable_logging()
        PyTrinamicMicro.logging_enabled = enabled

    @staticmethod
    def __init_logger():
        PyTrinamicMicro.__logger = logging.getLogger()
        formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
        PyTrinamicMicro.__logger.setLevel(PyTrinamicMicro.LOGGING_VERBOSITY)
        if(PyTrinamicMicro.LOGGING_CONSOLE):
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(formatter)
            PyTrinamicMicro.__logger.addHandler(consoleHandler)
            PyTrinamicMicro.__logging_handlers.append(consoleHandler)
        if(PyTrinamicMicro.LOGGING_FILE):
            fileHandler = logging.FileHandler(PyTrinamicMicro.LOGGING_FILE_NAME)
            fileHandler.setFormatter(formatter)
            PyTrinamicMicro.__logger.addHandler(fileHandler)
            PyTrinamicMicro.__logging_handlers.append(fileHandler)
