'''
Example using the MAX22531PMB

Created on 21.1.2022

@author: ABN
'''
#Paste into terminal to run: exec(open("PyTrinamicMicro/platforms/motionpy2/examples/modules/max/max22531pmb_example2.py").read())

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


while(True): 
    for cursor in '|/-\\':
        # Read PROD_ID Register and prints register contents in bits
        address,data = max22531pmb.read_Register(max22531pmb.ADC.PROD_ID_adr)
        print("Register {0}: {1}".format(hex(int(address,2)),int(data,2)))

        # Read ADC1 Register and prints register contents in bits
        address,data = max22531pmb.read_Register(max22531pmb.ADC.ADC1_adr)
        print("Register {0}: {1}".format(hex(int(address,2)),int(data,2)))

        # Read ADC1 Register and print LSBs and Voltage Value
        lsb,voltage = max22531pmb.read_ADC(1)
        print("ADC1 LSBs = {0}, Voltage = {1}V".format(int(lsb,2),voltage))

        # Read FADC1, FADC2, FADC3, FADC4, COUT_STATUS, COUT1, COUT2 Register and print conents in hex
        adc1,adc2,adc3,adc4,cout_status,cout1,cout2 = max22531pmb.read_Analog_CH_COUT_Status_Cout1_Cout2("true")
        print("FADC1:{0} FADC2:{1} FADC3:{2} FADC4:{3} COUT_STATUS:{4} COUT1_COMP:{5} COUT2_COMP:{6}".format(hex(int(adc1,2)),hex(int(adc2,2)),hex(int(adc3,2)),hex(int(adc4,2)),cout_status,cout1,cout2))

        # Read CONTROL Register and prints register contents in bits
        address,data = max22531pmb.read_Register(max22531pmb.ADC.CONTROL_adr)
        print("Control Register = {0}, value = {1}".format(hex(int(address)),data))

        # Read ADC1, ADC2, ADC3, ADC4, COUT_STATUS, COUT1, COUT2 Register and print conents in hex
        adc1,adc2,adc3,adc4,cout_status,cout1,cout2 = max22531pmb.read_Analog_CH_COUT_Status_Cout1_Cout2("false")
        print("ADC1:{0} ADC2:{1} ADC3:{2} ADC4:{3} COUT_STATUS:{4} COUT1_COMP:{5} COUT2_COMP:{6}".format(hex(int(adc1,2)),hex(int(adc2,2)),hex(int(adc3,2)),hex(int(adc4,2)),cout_status,cout1,cout2))

        # Confiure/ Enable Interrupts (SPIFRM, SPICRC)
        max22531pmb.Configure_Interrupt("ESPIFRM","enable")
        max22531pmb.Configure_Interrupt("ESPICRC","enable")		

        # Enable CRC
        print(max22531pmb.Control_CRC("enable"))

        # Read INTERRUPT_STATUS Register and prints register contents associated with status bits
        interrupt_bits = max22531pmb.read_interrupt()
        print("Interrupt bits: EOC:{0} , ADCF:{1} , FLD:{2} , SPIFRM:{3} , SPICRC:{4} , CO_POS_4:{5} , CO_POS_3:{6} , CO_POS_2:{7} , CO_POS_1:{8} , CO_NEG_4:{9} , CO_NEG_3:{10} , CO_NEG_2:{11} , CO_NEG_1:{12} ".format(interrupt_bits[0],interrupt_bits[1],interrupt_bits[2],interrupt_bits[3],interrupt_bits[4],interrupt_bits[5],interrupt_bits[6],interrupt_bits[7],interrupt_bits[8],interrupt_bits[9],interrupt_bits[10],interrupt_bits[11],interrupt_bits[12])) 


        # Read CONTROL Register and prints register contents in bits with CRC enabled
        address,data = max22531pmb.read_Register(max22531pmb.ADC.CONTROL_adr)
        print("Control Register = {0}, value = {1}".format(hex(int(address)),data))

        # Disable CRC
        print(max22531pmb.Control_CRC("disable"))

        # Read INTERRUPT_STATUS Register and prints register contents associated with status bits
        interrupt_bits = max22531pmb.read_interrupt()
        print("Interrupt bits: EOC:{0} , ADCF:{1} , FLD:{2} , SPIFRM:{3} , SPICRC:{4} , CO_POS_4:{5} , CO_POS_3:{6} , CO_POS_2:{7} , CO_POS_1:{8} , CO_NEG_4:{9} , CO_NEG_3:{10} , CO_NEG_2:{11} , CO_NEG_1:{12} ".format(interrupt_bits[0],interrupt_bits[1],interrupt_bits[2],interrupt_bits[3],interrupt_bits[4],interrupt_bits[5],interrupt_bits[6],interrupt_bits[7],interrupt_bits[8],interrupt_bits[9],interrupt_bits[10],interrupt_bits[11],interrupt_bits[12])) 


        # Read CONTROL Register and prints register contents in bits with CRC disabled
        address,data = max22531pmb.read_Register(max22531pmb.ADC.CONTROL_adr)
        print("Control Register = {0}, value = {1}".format(hex(int(address)),data))

        # Read INTERRUPT_STATUS Register and prints register contents associated with status bits
        interrupt_bits = max22531pmb.read_interrupt()
        print("Interrupt bits: EOC:{0} , ADCF:{1} , FLD:{2} , SPIFRM:{3} , SPICRC:{4} , CO_POS_4:{5} , CO_POS_3:{6} , CO_POS_2:{7} , CO_POS_1:{8} , CO_NEG_4:{9} , CO_NEG_3:{10} , CO_NEG_2:{11} , CO_NEG_1:{12} ".format(interrupt_bits[0],interrupt_bits[1],interrupt_bits[2],interrupt_bits[3],interrupt_bits[4],interrupt_bits[5],interrupt_bits[6],interrupt_bits[7],interrupt_bits[8],interrupt_bits[9],interrupt_bits[10],interrupt_bits[11],interrupt_bits[12])) 

        # Configure COUTHI(1-4) Registers with Mode and Input select and print hex data respectively
        max22531pmb.comparator_modes_inputSelect(1,0,0)
        max22531pmb.comparator_modes_inputSelect(2,0,1)
        max22531pmb.comparator_modes_inputSelect(3,1,0)
        max22531pmb.comparator_modes_inputSelect(4,1,1)
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTHI1_adr)
        print("COMP_HIGH_1 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTHI2_adr)
        print("COMP_HIGH_2 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTHI3_adr)
        print("COMP_HIGH_3 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTHI4_adr)
        print("COMP_HIGH_4 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))

        # Configure COUTHI(1-4) and COUTLO(1-4) Registers with Upper and Lower Treshold Values (in hex) and print hex data respectively
        max22531pmb.set_comparator_thres_hex(1,0x324,0xdf4)
        max22531pmb.set_comparator_thres_hex(2,0x419,0xe91)
        max22531pmb.set_comparator_thres_hex(3,0x2c4,0xe67)
        max22531pmb.set_comparator_thres_hex(4,0x3fb,0xf17)	
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTHI1_adr)
        print("COMP_HIGH_1 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTHI2_adr)
        print("COMP_HIGH_2 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTHI3_adr)
        print("COMP_HIGH_3 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTHI4_adr)
        print("COMP_HIGH_4 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTLO1_adr)
        print("COMP_LOW_1 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTLO2_adr)
        print("COMP_LOW_2 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTLO3_adr)
        print("COMP_LOW_3 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTLO4_adr)
        print("COMP_LOW_4 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))

        # Reset the Device
        max22531pmb.reset()

        # Read COUTHI(1-4) and COUTLO(1-4) Registers after Reset and print hex data respectively. Values are back to default states
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTHI1_adr)
        print("COMP_HIGH_1 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTHI2_adr)
        print("COMP_HIGH_2 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTHI3_adr)
        print("COMP_HIGH_3 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTHI4_adr)
        print("COMP_HIGH_4 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTLO1_adr)
        print("COMP_LOW_1 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTLO2_adr)
        print("COMP_LOW_2 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTLO3_adr)
        print("COMP_LOW_3 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTLO4_adr)
        print("COMP_LOW_4 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))		

        # Configure INTERRUPT_ENABLE register for respective interrupt bits and register contents in bits
        max22531pmb.Configure_Interrupt("EEOC", "enable")
        interrupt_ctrl_register = max22531pmb.read_Register(max22531pmb.ADC.INTERRUPT_ENABLE_adr)
        print("Interrupt Register Bits [15:0]",interrupt_ctrl_register)
        max22531pmb.Configure_Interrupt("EFLD", "enable")
        interrupt_ctrl_register = max22531pmb.read_Register(max22531pmb.ADC.INTERRUPT_ENABLE_adr)
        print("Interrupt Register Bits [15:0]",interrupt_ctrl_register)
        max22531pmb.Configure_Interrupt("ESPICRC", "enable")
        interrupt_ctrl_register = max22531pmb.read_Register(max22531pmb.ADC.INTERRUPT_ENABLE_adr)
        print("Interrupt Register Bits [15:0]",interrupt_ctrl_register)
        max22531pmb.Configure_Interrupt("EEOC", "disable")
        interrupt_ctrl_register = max22531pmb.read_Register(max22531pmb.ADC.INTERRUPT_ENABLE_adr)
        print("Interrupt Register Bits [15:0]",interrupt_ctrl_register)
        max22531pmb.Configure_Interrupt("EFLD", "disable")
        interrupt_ctrl_register = max22531pmb.read_Register(max22531pmb.ADC.INTERRUPT_ENABLE_adr)
        print("Interrupt Register Bits [15:0]",interrupt_ctrl_register)
        max22531pmb.Configure_Interrupt("ESPICRC", "disable")
        interrupt_ctrl_register = max22531pmb.read_Register(max22531pmb.ADC.INTERRUPT_ENABLE_adr)
        print("Interrupt Register Bits [15:0]",interrupt_ctrl_register)

        # Configure COUTHI1 and COUTLO1 Registers with Upper and Lower Treshold Values (in Volts) and Configure Mode
        # and Input Select and print hex data respectively
        max22531pmb.set_comparator_thres_volt(1,1,4.5)
        max22531pmb.comparator_modes_inputSelect(1,1,1)
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTHI1_adr)
        print("COMP_HIGH_1 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTLO1_adr)
        print("COMP_LOW_1 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        max22531pmb.comparator_modes_inputSelect(1,0,0)
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTHI1_adr)
        print("COMP_HIGH_1 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTLO1_adr)
        print("COMP_LOW_1 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))	

        # Enable CRC
        print(max22531pmb.Control_CRC("enable"))

        # Read INTERRUPT_STATUS Register and prints register contents associated with status bits
        interrupt_bits = max22531pmb.read_interrupt()
        print("Interrupt bits: EOC:{0} , ADCF:{1} , FLD:{2} , SPIFRM:{3} , SPICRC:{4} , CO_POS_4:{5} , CO_POS_3:{6} , CO_POS_2:{7} , CO_POS_1:{8} , CO_NEG_4:{9} , CO_NEG_3:{10} , CO_NEG_2:{11} , CO_NEG_1:{12} ".format(interrupt_bits[0],interrupt_bits[1],interrupt_bits[2],interrupt_bits[3],interrupt_bits[4],interrupt_bits[5],interrupt_bits[6],interrupt_bits[7],interrupt_bits[8],interrupt_bits[9],interrupt_bits[10],interrupt_bits[11],interrupt_bits[12])) 


        # Configure COUTHI1 and COUTLO1 Registers with Upper and Lower Treshold Values (in Volts) and Configure Mode
        # and Input Select and print hex data respectively with CRC Enabled
        max22531pmb.set_comparator_thres_volt(1,1,4.5)
        max22531pmb.comparator_modes_inputSelect(1,1,1)
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTHI1_adr)
        print("COMP_HIGH_1 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTLO1_adr)
        print("COMP_LOW_1 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        max22531pmb.comparator_modes_inputSelect(1,0,0)
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTHI1_adr)
        print("COMP_HIGH_1 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))
        address,data = max22531pmb.read_Register(max22531pmb.ADC.COUTLO1_adr)
        print("COMP_LOW_1 = {0}, value = {1}".format(hex(int(address)),hex(int(data,2))))

        # Perform Burst Read and print ADCx, FADCx contects in hex and INTERRUPT_STATUS contents in bits
        adc1,adc2,adc3,adc4,int_status = max22531pmb.Burst_read("ADC")
        print("ADC1:{0} ADC2:{1} ADC3:{2} ADC4:{3} INTERRUPT_STATUS:{4} ".format(hex(int(adc1,2)),hex(int(adc2,2)),hex(int(adc3,2)),hex(int(adc4,2)),int_status))

        # Disable CRC
        print(max22531pmb.Control_CRC("disable"))

        # Read INTERRUPT_STATUS Register and prints register contents associated with status bits
        interrupt_bits = max22531pmb.read_interrupt()
        print("Interrupt bits: EOC:{0} , ADCF:{1} , FLD:{2} , SPIFRM:{3} , SPICRC:{4} , CO_POS_4:{5} , CO_POS_3:{6} , CO_POS_2:{7} , CO_POS_1:{8} , CO_NEG_4:{9} , CO_NEG_3:{10} , CO_NEG_2:{11} , CO_NEG_1:{12} ".format(interrupt_bits[0],interrupt_bits[1],interrupt_bits[2],interrupt_bits[3],interrupt_bits[4],interrupt_bits[5],interrupt_bits[6],interrupt_bits[7],interrupt_bits[8],interrupt_bits[9],interrupt_bits[10],interrupt_bits[11],interrupt_bits[12])) 

        # Perform Burst Read and print ADCx, FADCx contects in hex and INTERRUPT_STATUS contents in bits with CRC Disabled
        fadc1,fadc2,fadc3,fadc4,int_status = max22531pmb.Burst_read("FADC")
        print("FADC1:{0} FADC2:{1} FADC3:{2} FADC4:{3} INTERRUPT_STATUS:{4} ".format(hex(int(fadc1,2)),hex(int(fadc2,2)),hex(int(fadc3,2)),hex(int(fadc4,2)),int_status))

		# Read COUT_STATUS Bits
        data = max22531pmb.read_COUT_Status()
        print("COUT STATUS: CO_4:{0} , CO_3:{1} , CO_2:{2} , CO_1:{3} ".format(data[0],data[1],data[2],data[3]))

		# Reset the device
        max22531pmb.reset()
        time.sleep(1)
