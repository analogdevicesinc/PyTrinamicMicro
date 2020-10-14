# Operational Guide

This is a guide on how to use the PyTrinamicMicro specific modules.  
For a MicroPython specific guide, please refer to [docs.micropython.org](https://docs.micropython.org).

## Getting started

1. Prepare the target system to run MicroPython. If there is already a MicroPython port available for the
target system, there might be a guide for that in the official MicroPython docs.
Make sure to also install the Serial Port Drivers for USB communication to work.
2. If the target platform is a microcontroller, there might be not enough space for the packages in the internal flash.
In that case, some kind of memory (i.e. SD card) needs to be provided and properly mounted.
Refer to the MicroPython docs on how to do this.
3. If the target platform is a microcontroller, plug in the MicroPython board to the PC.
It should already get detected as mass storage device, with the SD card mounted directly to the root. 
4. Invoke the installation script `install.py`. For full installation, run the command `python install.py D:\`,
assuming `python` is properly linked to your python binary and `D:\` is the installation directory.
5. Soft-Reset MicroPython by restarting it, or, if it is a microcontroller, hard-reset the microcontroller
with a `low` signal on the `NRST` pin.
6. If the target system is a microcontroller, connect to the corresponding serial port via terminal.
This might be `COMX` for Windows (determine *X* in the Device Manager), or `/dev/ttyACMX`
(determine *X* in the mounted devices in `/dev`) for Linux.
7. Now, being in the Python shell, any MicroPython compatible statement can be interpreted.
The PyTrinamicMicro package can be used. 
Examples can be executed by e.g. `exec(open("PyTrinamicMicro/examples/modules/TMCM1270/TMCM1270_rotate.py").read())`.
