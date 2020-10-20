'''
Install script to copy the required files in correct structure on the SD card.

Created on 13.10.2020

@author: LK
'''

import argparse
import os
import shutil
import logging

args = None
logger = None

def clean_pytrinamic():
    logger.info("Cleaning PyTrinamic ...")
    shutil.rmtree(os.path.join(args.path[0], "PyTrinamic"), ignore_errors=True)
    logger.info("PyTrinamic cleaned.")

def clean_pytrinamicmicro():
    logger.info("Cleaning PyTrinamicMicro ...")
    shutil.rmtree(os.path.join(args.path[0], "PyTrinamicMicro"), ignore_errors=True)
    logger.info("PyTrinamicMicro cleaned.")

def clean_lib():
    logger.info("Cleaning libraries ...")

    logger.info("Cleaning logging ...")
    shutil.rmtree(os.path.join(args.path[0], "logging"), ignore_errors=True)
    logger.info("logging cleaned.")

    logger.info("Cleaning argparse ...")
    shutil.rmtree(os.path.join(args.path[0], "argparse"), ignore_errors=True)
    logger.info("argparse cleaned.")

    logger.info("Libraries cleaned.")

def clean_full():
    logger.info("Cleaning ...")
    clean_pytrinamic()
    clean_pytrinamicmicro()
    clean_lib()
    logger.info("Cleaned.")

def install_pytrinamic():
    if(args.clean):
        clean_pytrinamic()
    logger.info("Installing PyTrinamic ...")
    shutil.copytree("PyTrinamic/PyTrinamic", os.path.join(args.path[0], "PyTrinamic"))
    logger.info("PyTrinamic installed.")

def install_pytrinamicmicro():
    if(args.clean):
        clean_pytrinamicmicro()
    logger.info("Installing PyTrinamicMicro ...")
    shutil.copytree("PyTrinamicMicro", os.path.join(args.path[0], "PyTrinamicMicro"))
    logger.info("PyTrinamicMicro installed.")

def install_lib():
    if(args.clean):
        clean_lib()

    logger.info("Installing libraries ...")

    logger.info("Installing logging ...")
    shutil.copytree("pycopy-lib/logging/logging", os.path.join(args.path[0], "logging"))
    logger.info("logging installed.")

    logger.info("Installing argparse ...")
    shutil.copytree("pycopy-lib/argparse/argparse", os.path.join(args.path[0], "argparse"))
    logger.info("argparse installed.")

    logger.info("Libraries installed.")

def install_full():
    logger.info("Installing full ...")
    install_pytrinamic()
    install_pytrinamicmicro()
    install_lib()
    logger.info("Fully installed.")

SELECTION_MAP = {
    "full": install_full,
    "pytrinamic": install_pytrinamic,
    "pytrinamicmicro": install_pytrinamicmicro,
    "lib": install_lib
}

# Initialize install logger

logger = logging.getLogger(__name__)
formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
logger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

# Argument parsing and mode execution

parser = argparse.ArgumentParser(description='Install the required files in correct structure on the SD card.')
parser.add_argument('path', metavar="path", type=str, nargs=1, default=".",
    help='Path to the root of the SD card (default: %(default)s).')
parser.add_argument('-s', "--selection", dest='selection', action='store', nargs="*", type=str.lower,
    choices=['full', 'pytrinamic', 'pytrinamicmicro', 'lib'],
    default=['full'], help='Install selection (default: %(default)s).')
parser.add_argument('-c', "--clean", dest='clean', action='store_true', help='Clean module target directory before installing it there (default: %(default)s).')

args = parser.parse_args()

os.makedirs(args.path[0], exist_ok=True)

for s in args.selection:
    SELECTION_MAP.get(s)()

logger.info("Done.")
