'''
Created on 06.10.2020

@author: LK
'''


from PyTrinamicMicro.connections.uart_tmcl_interface import uart_tmcl_interface


class rs232_tmcl_interface(uart_tmcl_interface):

    def __init__(self, baudrate=9600, hostID=2, moduleID=1, debug=False):
        super().__init__(2, baudrate, hostID, moduleID, debug)
