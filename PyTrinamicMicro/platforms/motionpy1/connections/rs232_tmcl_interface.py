'''
Created on 06.10.2020

@author: LK
'''


from PyTrinamicMicro.platforms.motionpy1.connections.uart_tmcl_interface import uart_tmcl_interface


class rs232_tmcl_interface(uart_tmcl_interface):

    def __init__(self, port=2, data_rate=115200, host_id=2, module_id=1, debug=False):
        super().__init__(port, data_rate, host_id, module_id, debug)

    @staticmethod
    def available_ports():
        return set([2])
