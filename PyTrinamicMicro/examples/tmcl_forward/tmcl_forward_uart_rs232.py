'''
Forward from UART host to RS232 module.

Created on 07.10.2020

@author: LK
'''

from PyTrinamicMicro.connections.tmcl_host_interface import tmcl_host_interface
from PyTrinamicMicro.connections.rs232_tmcl_interface import rs232_tmcl_interface
from PyTrinamicMicro.connections.uart_tmcl_interface import uart_tmcl_interface
from PyTrinamicMicro.TMCL_Forwarder import TMCL_Forwarder

forwarder = TMCL_Forwarder(tmcl_host_interface(uart_tmcl_interface()), rs232_tmcl_interface())

while(True):
    forwarder.forward()
