from pyb import SPI
from pyb import Pin
import struct
from PyTrinamic.helpers import TMC_helpers

class MCP23S08(object):

    ADDRESS = 0b0100000
    STRUCT = "BBB"
    REGISTERS = {
        "IODIR": (0x00, 0b11111111),
        "IPOL": (0x01, 0b00000000),
        "GPINTEN": (0x02, 0b00000000),
        "DEFVAL": (0x03, 0b00000000),
        "INTCON": (0x04, 0b00000000),
        "IOCON": (0x05, 0b00000000),
        "GPPU": (0x06, 0b00000000),
        "INTF": (0x07, 0b00000000),
        "INTCAP": (0x08, 0b00000000),
        "GPIO": (0x09, 0b00000000),
        "OLAT": (0x0A, 0b00000000)
    }

    def __init__(self, cs=Pin.cpu.A4):
        self.__cs = Pin(cs, Pin.OUT_PP)
        self.__cs.high()
        self.__spi = SPI(1, SPI.MASTER, baudrate=10000, polarity=1, phase=1)
        self.reset()

    def reset(self):
        for reg in MCP23S08.REGISTERS.values():
            self.write_register(reg, reg[1])

    def read_register(self, register):
        buf = bytearray(struct.pack(MCP23S08.STRUCT, (MCP23S08.ADDRESS << 1) | 1, register[0], 0))
        self.__cs.low()
        self.__spi.send_recv(buf, buf)
        self.__cs.high()
        return buf[2]

    def write_register(self, register, value):
        buf = bytearray(struct.pack(MCP23S08.STRUCT, MCP23S08.ADDRESS << 1, register[0], value))
        self.__cs.low()
        self.__spi.send_recv(buf, buf)
        self.__cs.high()

    def set_directions(self, directions):
        self.write_register(MCP23S08.REGISTERS["IODIR"], directions)

    def get_directions(self):
        return self.read_register(MCP23S08.REGISTERS["IODIR"])

    def set_direction(self, idx, direction):
        self.set_directions(TMC_helpers.field_set(self.get_directions(), (1 << idx), idx, direction))

    def get_direction(self, idx):
        return TMC_helpers.field_get(self.get_directions(), (1 << idx), idx)

    def set_pullups(self, pullups):
        self.write_register(MCP23S08.REGISTERS["GPPU"], pullups)

    def get_pullups(self):
        return self.read_register(MCP23S08.REGISTERS["GPPU"])

    def set_pullup(self, idx, pullup):
        self.set_pullups(TMC_helpers.field_set(self.get_pullups(), (1 << idx), idx, pullup))

    def get_pullup(self, idx):
        return TMC_helpers.field_get(self.get_pullups(), (1 << idx), idx)

    def set_gpios(self, gpios):
        self.write_register(MCP23S08.REGISTERS["GPIO"], gpios)

    def get_gpios(self):
        return self.read_register(MCP23S08.REGISTERS["GPIO"])

    def set_gpio(self, idx, gpio):
        self.set_gpios(TMC_helpers.field_set(self.get_gpios(), (1 << idx), idx, gpio))

    def get_gpio(self, idx):
        return TMC_helpers.field_get(self.get_gpios(), (1 << idx), idx)
