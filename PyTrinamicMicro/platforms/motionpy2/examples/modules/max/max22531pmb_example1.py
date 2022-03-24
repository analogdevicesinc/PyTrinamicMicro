'''
Example using the MAX22531PMB

Created on 21.1.2022

@author: ABN
'''
#Paste into terminal to run: exec(open("PyTrinamicMicro/platforms/motionpy2/examples/modules/max/max22531pmb_example1.py").read())

from PyTrinamicMicro.platforms.motionpy2.modules.max.max22531 import MAX22531, MAX22531PMB
from pyb import Pin
import time
import logging


# Prepare Logger
logger = logging.getLogger(__name__)
logger.info("Reading ADC")

pmod0 = dict({
    "pin_cs"            : Pin.cpu.A4,
    "pin_COUT2"         : Pin.cpu.B0,
    "pin_COUT1"        : Pin.cpu.C13,
    "pin_INTB"         : Pin.cpu.C5,
    "spi" : 1
    })

pmod1 = dict({
    "pin_cs"            : Pin.cpu.B12,
    "pin_COUT2"         : Pin.cpu.C4,
    "pin_COUT1"        : Pin.cpu.C6,
    "pin_INTB"         : Pin.cpu.C3,
    "spi" : 2
    })

'''Change pmod connector here'''
connector = pmod0
max22531pmb = MAX22531PMB(**connector)
#test script to communicate with PMB

answer = max22531pmb.device_init()
print("MAX22531 status = {0} \r".format(answer))
if(str(answer) == "1"):
    print("Device Recognized")
else:
    print("Device Not recognized")
#Configure COUTHI(1-4) and COUTLO(1-4) Registers with different input modes, input select and threshold values
max22531pmb.comparator_modes_inputSelect(1,0,0)
max22531pmb.comparator_modes_inputSelect(2,0,1)
max22531pmb.comparator_modes_inputSelect(3,1,0)
max22531pmb.comparator_modes_inputSelect(4,1,1)
max22531pmb.set_comparator_thres_volt(1,1,4.5)
max22531pmb.set_comparator_thres_volt(2,1,4.5)
max22531pmb.set_comparator_thres_volt(3,1,4.5)
max22531pmb.set_comparator_thres_volt(4,1,4.5)

while(True): 
    for cursor in '|/-\\':
        # Read ADC1 Register and print LSBs and Voltage Value
        lsb,voltage = max22531pmb.read_ADC(1)
        print("ADC1 LSBs = {0}, Voltage = {1}V".format(int(lsb,2),voltage))
        lsb,voltage = max22531pmb.read_ADC(2)
        print("ADC2 LSBs = {0}, Voltage = {1}V".format(int(lsb,2),voltage))        
        lsb,voltage = max22531pmb.read_ADC(3)
        print("ADC3 LSBs = {0}, Voltage = {1}V".format(int(lsb,2),voltage))
        lsb,voltage = max22531pmb.read_ADC(4)
        print("ADC4 LSBs = {0}, Voltage = {1}V".format(int(lsb,2),voltage))
        # Read FADC1, FADC2, FADC3, FADC4, COUT_STATUS, COUT1, COUT2 Register and print conents in hex
        adc1,adc2,adc3,adc4,cout_status,cout1,cout2 = max22531pmb.read_Analog_CH_COUT_Status_Cout1_Cout2("true")
        print("FADC1:{0} FADC2:{1} FADC3:{2} FADC4:{3} COUT_STATUS:{4} COUT1_COMP:{5} COUT2_COMP:{6}".format(hex(int(adc1,2)),hex(int(adc2,2)),hex(int(adc3,2)),hex(int(adc4,2)),cout_status,cout1,cout2))        
        time.sleep(0.1)