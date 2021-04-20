'''
This file implements an example for using the MAX22190PMB in SPI Mode 1. 
It displays the input read and wire break readout in the terminal.
For further details on MAX22190PMB refer to the data sheet.

Created on 25.02.2021

@author: JH
'''

logger = logging.getLogger(__name__)
logger.info("MAX22190PMB example running")


pins = dict({
    "pin_cs"    :   Pin.cpu.C0,
    "spi"       :   1,
    "fault_pin" :   Pin.cpu.C1,
    "ready_pin" :   Pin.cpu.A13, 
    "latch_pin" :   Pin.cpu.A14,
    })

module = MAX22190(pins["pin_cs"],pins["spi"],pins["fault_pin"],pins["ready_pin"],pins["latch_pin"])
#clear fault registers
module.read_write_register(0x04,1,0x00)
module.read_write_register(0x1C,1,0x00)
#enable wire break detection 
module.read_write_register(module.MAX22190_FILTER_IN_1,1,0x18)
module.read_write_register(module.MAX22190_FILTER_IN_2,1,0x18)
module.read_write_register(module.MAX22190_FILTER_IN_3,1,0x18)
module.read_write_register(module.MAX22190_FILTER_IN_4,1,0x18)
module.read_write_register(module.MAX22190_FILTER_IN_5,1,0x18)
module.read_write_register(module.MAX22190_FILTER_IN_6,1,0x18)
module.read_write_register(module.MAX22190_FILTER_IN_7,1,0x18)
module.read_write_register(module.MAX22190_FILTER_IN_8,1,0x18)

description = """\nThis scripts displays the digital channel inputs as well as the wire break detection states.
Channel input       => 0: Channel is driven low;            1: Channel is driven high.
Wire break detection=> 0: wire break condition detected;    1: no wire break condition detected.\n """
print(description)
legend = "Channel nr.: " + "12345678"+ ";       Channel nr.: " + "12345678"
print(legend)
while(True):
    for cursor in '|/-\\':
        input_states = module.get_digital_input_states()
        wire_breaks  = module.get_wire_break_states()
        fault_pin =  module.get_fault_pin()
        ready_pin = module.get_ready_pin()
        latched   = module.get_latch_pin()
        text =  cursor+" IO states: " + ''.join(str(e) for e in input_states)+ "; Wire Break states: " + ''.join(str(e) for e in wire_breaks)  +" ready:"+ str(ready_pin)+" fault:"+  str(fault_pin) +" latched:"+ str(latched)
        print(text, end='\r')
        time.sleep(0.25)

