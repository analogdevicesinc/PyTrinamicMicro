'''
Bridge from UART host to RS232 module.

Created on 07.10.2020

@author: LK
'''

from PyTrinamicMicro.connections.tmcl_host_interface import tmcl_host_interface
from PyTrinamicMicro.connections.rs232_tmcl_interface import rs232_tmcl_interface
from PyTrinamicMicro.connections.uart_tmcl_interface import uart_tmcl_interface
from PyTrinamicMicro.TMCL_Bridge import TMCL_Bridge

host = uart_tmcl_interface()
module = rs232_tmcl_interface()
bridge = TMCL_Bridge(tmcl_host_interface(host), module)

while(not(bridge.process())):
    pass

host.close()
module.close()
