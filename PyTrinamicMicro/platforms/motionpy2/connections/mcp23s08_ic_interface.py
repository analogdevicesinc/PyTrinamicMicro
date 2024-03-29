################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

'''
Created on 05.10.2020

@author: LK
'''

from PyTrinamicMicro.platforms.motionpy2.modules.MCP23S08 import MCP23S08

class mcp23s08_ic_interface(object):

    def __init__(self, mcp23s08, spi=SPI(1, SPI.MASTER, baudrate=10000, polarity=1, phase=1), cs=4):
        self.__spi = spi
        self.__cs = cs
        self.__mcp23s08 = mcp23s08

        self.__mcp23s08.set_direction(self.__cs, 0)
        self.__mcp23s08.set_gpio(self.__cs, 1)

    def send(self, buf):
        self.__mcp23s08.set_gpio(self.__cs, 0)
        self.__spi.send(buf)
        self.__mcp23s08.set_gpio(self.__cs, 1)

    def send_recv(self, buf_send, buf_recv):
        self.__mcp23s08.set_gpio(self.__cs, 0)
        self.__spi.send_recv(buf_send, buf_recv)
        self.__mcp23s08.set_gpio(self.__cs, 1)
