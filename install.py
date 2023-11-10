################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
Install script to copy the required files in correct structure on the SD card.

Created on 13.10.2020

@author: LK
'''

import argparse
import os
import shutil
import logging

MPY_CROSS = "mpy-cross"

# Initialize install logger

logger = logging.getLogger(__name__)
formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
logger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

def clean_pytrinamic(path):
    logger.info("Cleaning PyTrinamic ...")
    shutil.rmtree(os.path.join(path, "PyTrinamic"), ignore_errors=True)
    logger.info("PyTrinamic cleaned.")

def clean_motionpy(path):
    logger.info("Cleaning MotionPy ...")
    shutil.rmtree(os.path.join(path, "PyTrinamicMicro", "platforms", "motionpy1"), ignore_errors=True)
    logger.info("MotionPy cleaned.")

def clean_pytrinamicmicro_api(path):
    logger.info("Cleaning PyTrinamicMicro API ...")
    shutil.rmtree(os.path.join(path, "PyTrinamicMicro", "connections"), ignore_errors=True)
    shutil.rmtree(os.path.join(path, "PyTrinamicMicro", "examples"), ignore_errors=True)
    if(os.path.exists(os.path.join(path, "PyTrinamicMicro", "__init__.py"))):
        os.remove(os.path.join(path, "PyTrinamicMicro", "__init__.py"))
    if(os.path.exists(os.path.join(path, "PyTrinamicMicro", "PyTrinamicMicro.py"))):
        os.remove(os.path.join(path, "PyTrinamicMicro", "PyTrinamicMicro.py"))
    if(os.path.exists(os.path.join(path, "PyTrinamicMicro", "tmcl_bootloader.py"))):
        os.remove(os.path.join(path, "PyTrinamicMicro", "tmcl_bootloader.py"))
    if(os.path.exists(os.path.join(path, "PyTrinamicMicro", "TMCL_Bridge.py"))):
        os.remove(os.path.join(path, "PyTrinamicMicro", "TMCL_Bridge.py"))
    if(os.path.exists(os.path.join(path, "PyTrinamicMicro", "TMCL_Slave.py"))):
        os.remove(os.path.join(path, "PyTrinamicMicro", "TMCL_Slave.py"))
    logger.info("PyTrinamicMicro API cleaned.")

def clean_pytrinamicmicro(path):
    logger.info("Cleaning PyTrinamicMicro ...")
    shutil.rmtree(os.path.join(path, "PyTrinamicMicro"), ignore_errors=True)
    logger.info("PyTrinamicMicro cleaned.")

def clean_lib(path):
    logger.info("Cleaning libraries ...")

    logger.info("Cleaning logging ...")
    shutil.rmtree(os.path.join(path, "logging"), ignore_errors=True)
    logger.info("logging cleaned.")

    logger.info("Cleaning argparse ...")
    shutil.rmtree(os.path.join(path, "argparse"), ignore_errors=True)
    logger.info("argparse cleaned.")

    logger.info("Libraries cleaned.")

def clean_full(path):
    logger.info("Cleaning ...")
    clean_pytrinamic(path)
    clean_pytrinamicmicro(path)
    clean_lib(path)
    logger.info("Cleaned.")

def compile_recursive(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in [f for f in filenames if f.endswith(".py")]:
            current = os.path.join(dirpath, filename)
            logger.info("Compiling {}".format(current))
            os.system("{} {}".format(MPY_CROSS, current))

def install_pytrinamic(path, compile, clean):
    if(clean):
        clean_pytrinamic(path)
    base = os.path.join("PyTrinamic", "PyTrinamic")
    logger.info("Installing PyTrinamic ...")
    if(compile):
        logger.info("Compiling PyTrinamic ...")
        compile_recursive(base)
        logger.info("PyTrinamic compiled.")
    logger.info("Copying PyTrinamic ...")
    shutil.copytree(base, os.path.join(path, "PyTrinamic"), ignore=shutil.ignore_patterns("*.py" if compile else "*.mpy"))
    logger.info("PyTrinamic copied.")
    logger.info("PyTrinamic installed.")

def install_motionpy1_boot(path, compile, clean):
    del clean
    logger.info("Installing MotionPy v1 boot ...")
    shutil.copy(os.path.join("PyTrinamicMicro", "platforms", "motionpy1", "boot.py"), path)
    logger.info("MotionPy v1 boot installed.")

def install_motionpy1_main(path, compile, clean):
    del clean
    logger.info("Installing MotionPy v1 main ...")
    shutil.copy(os.path.join("PyTrinamicMicro", "platforms", "motionpy1", "main.py"), path)
    logger.info("MotionPy v1 main installed.")

def install_motionpy1(path, compile, clean):
    if(clean):
        clean_motionpy(path)
    base = os.path.join("PyTrinamicMicro", "platforms", "motionpy1")
    logger.info("Installing platform MotionPy v1 ...")
    os.makedirs(os.path.join(path, "PyTrinamicMicro", "platforms"), exist_ok=True)
    if(compile):
        logger.info("Compiling MotionPy v1 ...")
        compile_recursive(base)
        logger.info("MotionPy v1 compiled.")
    logger.info("Copying MotionPy v1 ...")
    shutil.copytree(base, os.path.join(path, "PyTrinamicMicro", "platforms", "motionpy1"), ignore=shutil.ignore_patterns("*.py" if compile else "*.mpy"))
    logger.info("MotionPy v1 copied.")
    logger.info("MotionPy v1 installed.")

def install_motionpy2_boot(path, compile, clean):
    del clean
    logger.info("Installing MotionPy v2 boot ...")
    shutil.copy(os.path.join("PyTrinamicMicro", "platforms", "motionpy2", "boot.py"), path)
    logger.info("MotionPy v2 boot installed.")

def install_motionpy2_main(path, compile, clean):
    del clean
    logger.info("Installing MotionPy v2 main ...")
    shutil.copy(os.path.join("PyTrinamicMicro", "platforms", "motionpy2", "main.py"), path)
    logger.info("MotionPy v2 main installed.")

def install_motionpy2_test(path, compile, clean):
    del clean
    logger.info("Installing MotionPy v2 test ...")
    shutil.copy(os.path.join("PyTrinamicMicro", "platforms", "motionpy2", "main_test.py"), path)
    shutil.move(os.path.join(path, "main_test.py"), os.path.join(path, "main.py"))
    logger.info("MotionPy v2 test installed.")

def install_motionpy2(path, compile, clean):
    if(clean):
        clean_motionpy(path)
    base = os.path.join("PyTrinamicMicro", "platforms", "motionpy2")
    logger.info("Installing platform MotionPy v2 ...")
    os.makedirs(os.path.join(path, "PyTrinamicMicro", "platforms"), exist_ok=True)
    if(compile):
        logger.info("Compiling MotionPy v2 ...")
        compile_recursive(base)
        logger.info("MotionPy v2 compiled.")
    logger.info("Copying MotionPy v2 ...")
    shutil.copytree(base, os.path.join(path, "PyTrinamicMicro", "platforms", "motionpy2"), ignore=shutil.ignore_patterns("*.py" if compile else "*.mpy"))
    logger.info("MotionPy v2 copied.")
    logger.info("MotionPy v2 installed.")

def install_pytrinamicmicro_api(path, compile, clean):
    if(clean):
        clean_pytrinamicmicro_api(path)
    logger.info("Installing PyTrinamicMicro API ...")
    shutil.copytree(os.path.join("PyTrinamicMicro", "connections"), os.path.join(path, "PyTrinamicMicro", "connections"))
    shutil.copy(os.path.join("PyTrinamicMicro", "__init__.py"), os.path.join(path, "PyTrinamicMicro"))
    shutil.copy(os.path.join("PyTrinamicMicro", "PyTrinamicMicro.py"), os.path.join(path, "PyTrinamicMicro"))
    shutil.copy(os.path.join("PyTrinamicMicro", "tmcl_bootloader.py"), os.path.join(path, "PyTrinamicMicro"))
    shutil.copy(os.path.join("PyTrinamicMicro", "TMCL_Bridge.py"), os.path.join(path, "PyTrinamicMicro"))
    shutil.copy(os.path.join("PyTrinamicMicro", "TMCL_Slave.py"), os.path.join(path, "PyTrinamicMicro"))
    logger.info("PyTrinamicMicro API installed.")

def install_pytrinamicmicro(path, compile, clean):
    if(clean):
        clean_pytrinamicmicro(path)
    base = "PyTrinamicMicro"
    logger.info("Installing PyTrinamicMicro ...")
    if(compile):
        logger.info("Compiling PyTrinamicMicro ...")
        compile_recursive(base)
        logger.info("PyTrinamicMicro compiled.")
    logger.info("Copying PyTrinamicMicro ...")
    shutil.copytree(base, os.path.join(path, "PyTrinamicMicro"), ignore=shutil.ignore_patterns("*.py" if compile else "*.mpy"))
    logger.info("PyTrinamicMicro copied.")
    logger.info("PyTrinamicMicro installed.")

def install_lib(path, compile, clean):
    if(clean):
        clean_lib(path)

    logger.info("Installing libraries ...")

    logger.info("Installing logging ...")
    base = os.path.join("pycopy-lib", "logging", "logging")
    if(compile):
        logger.info("Compiling logging ...")
        compile_recursive(base)
        logger.info("logging compiled.")
    logger.info("Copying logging ...")
    shutil.copytree(os.path.join("pycopy-lib", "logging", "logging"), os.path.join(path, "logging"), ignore=shutil.ignore_patterns("*.py" if compile else "*.mpy"))
    logger.info("logging copied.")
    logger.info("logging installed.")

    logger.info("Installing argparse ...")
    base = os.path.join("pycopy-lib", "argparse", "argparse")
    if(compile):
        logger.info("Compiling argparse ...")
        compile_recursive(base)
        logger.info("argparse compiled.")
    logger.info("Copying argparse ...")
    shutil.copytree(os.path.join("pycopy-lib", "argparse", "argparse"), os.path.join(path, "argparse"), ignore=shutil.ignore_patterns("*.py" if compile else "*.mpy"))
    logger.info("argparse copied.")
    logger.info("argparse installed.")

    logger.info("Libraries installed.")

def install_full(path, compile, clean):
    logger.info("Installing full ...")
    install_pytrinamic(path, compile, clean)
    install_pytrinamicmicro(path, compile, clean)
    install_lib(path, compile, clean)
    logger.info("Fully installed.")

SELECTION_MAP = {
    "full": install_full,
    "pytrinamic": install_pytrinamic,
    "pytrinamicmicro": install_pytrinamicmicro,
    "pytrinamicmicro-full": install_pytrinamicmicro,
    "pytrinamicmicro-api": install_pytrinamicmicro_api,
    "motionpy1": install_motionpy1,
    "motionpy1-boot": install_motionpy1_boot,
    "motionpy1-main": install_motionpy1_main,
    "motionpy2": install_motionpy2,
    "motionpy2-boot": install_motionpy2_boot,
    "motionpy2-main": install_motionpy2_main,
    "motionpy2-test": install_motionpy2_test,
    "lib": install_lib
}

# Argument parsing and mode execution

parser = argparse.ArgumentParser(description='Install the required files in correct structure on the SD card.')
parser.add_argument('path', metavar="path", type=str, nargs=1, default=".",
    help='Path to the root of the SD card (default: %(default)s).')
parser.add_argument('-s', "--selection", dest='selection', action='store', nargs="*", type=str.lower,
    choices=SELECTION_MAP.keys(),
    default=['full'], help='Install selection (default: %(default)s).')
parser.add_argument('-c', "--clean", dest='clean', action='store_true', help='Clean module target directory before installing it there (default: %(default)s).')
parser.add_argument("--compile", dest='compile', action='store_true', help='Compile every module (default: %(default)s).')

args = parser.parse_args()

os.makedirs(args.path[0], exist_ok=True)

for s in args.selection:
    SELECTION_MAP.get(s)(args.path[0], args.compile, args.clean)

logger.info("Done.")
