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
    def script(child, identifier):
        return compile(open(child._MAP_SCRIPT.get(identifier.lower())).read(), "<string>", "exec")

    @staticmethod
    def test(child, identifier):
        return compile(open(child._MAP_TEST.get(identifier.lower())).read(), "<string>", "exec")

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
