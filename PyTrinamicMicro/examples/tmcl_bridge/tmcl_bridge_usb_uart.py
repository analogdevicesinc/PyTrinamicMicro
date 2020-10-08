'''
Bridge from USB host to UART module.

Created on 08.10.2020

@author: LK
'''

from PyTrinamicMicro.connections.tmcl_host_interface import tmcl_host_interface
from PyTrinamicMicro.connections.uart_tmcl_interface import uart_tmcl_interface
from PyTrinamicMicro.connections.usb_vcp_tmcl_interface import usb_vcp_tmcl_interface
from PyTrinamicMicro.TMCL_Bridge import TMCL_Bridge
from PyTrinamic.TMCL import TMCL_Command

host = usb_vcp_tmcl_interface()
module = uart_tmcl_interface()
bridge = TMCL_Bridge(tmcl_host_interface(host), module)

while(not(bridge.process())):
    pass

host.close()
module.close()

print("Bridge stopped.")
