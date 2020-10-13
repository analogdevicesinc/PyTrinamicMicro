'''
PyTrinamicMicro root class, used for settings etc.

Created on 13.10.2020

@author: LK
'''

import logging

class PyTrinamicMicro(object):

    LOGGING_VERBOSITY = logging.DEBUG
    LOGGING_CONSOLE = False
    LOGGING_FILE = True
    LOGGING_FILE_NAME = "{}.log".format(__module__)

    @staticmethod
    def init():
        logger = PyTrinamicMicro.__init_logger()
        logger.debug("Root logger initialized.")
        logger.debug("PyTrinamicMicro initialized.")

    @staticmethod
    def __init_logger():
        logger = logging.getLogger()
        formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
        logger.setLevel(PyTrinamicMicro.LOGGING_VERBOSITY)
        if(PyTrinamicMicro.LOGGING_CONSOLE):
            consoleHandler = logging.StreamHandler()
            consoleHandler.setLevel(PyTrinamicMicro.LOGGING_VERBOSITY)
            consoleHandler.setFormatter(formatter)
            logger.addHandler(consoleHandler)
        if(PyTrinamicMicro.LOGGING_FILE):
            fileHandler = logging.FileHandler(PyTrinamicMicro.LOGGING_FILE_NAME)
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)
        return logger
