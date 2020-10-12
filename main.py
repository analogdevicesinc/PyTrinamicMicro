'''
MicroPython main file.
Place as main.py at the root of the Flash memory.

Created on 12.10.2020

@author: LK
'''

# Imports
import logging

# Constants
LOGGING_VERBOSITY = logging.DEBUG
LOGGING_CONSOLE = True
LOGGING_FILE = True
LOGGING_FILE_NAME = "global.log"

# Logging setup

logger = logging.getLogger(__name__)
formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
logger.setLevel(LOGGING_VERBOSITY)
if(LOGGING_CONSOLE):
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(LOGGING_VERBOSITY)
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
if(LOGGING_FILE):
    fileHandler = logging.FileHandler(LOGGING_FILE_NAME)
    fileHandler.setLevel(LOGGING_VERBOSITY)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
