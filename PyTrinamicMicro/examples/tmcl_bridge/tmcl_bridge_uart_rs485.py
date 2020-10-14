'''
Bridge from UART host to RS485 module.

Created on 14.10.2020

@author: LK
'''

from PyTrinamicMicro.connections.tmcl_host_interface import tmcl_host_interface
from PyTrinamicMicro.connections.rs485_tmcl_interface import rs485_tmcl_interface
from PyTrinamicMicro.connections.uart_tmcl_interface import uart_tmcl_interface
from PyTrinamicMicro.TMCL_Bridge import TMCL_Bridge

host = uart_tmcl_interface()
module = rs485_tmcl_interface()
bridge = TMCL_Bridge(host, module)

while(not(bridge.process())):
    pass

host.close()
module.close()

print("Bridge stopped.")
