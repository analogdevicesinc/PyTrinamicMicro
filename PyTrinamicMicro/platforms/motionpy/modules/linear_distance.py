from PyTrinamic.ic.TMC5130.TMC5130 import TMC5130
from PyTrinamicMicro.platforms.motionpy.connections.uart_ic_interface import uart_ic_interface
from PyTrinamicMicro.platforms.motionpy.modules.hc_sr04_multi import hc_sr04_multi
from PyTrinamicMicro.platforms.motionpy.modules.MCP23S08 import MCP23S08
import logging

class linear_distance(object):

    def __init__(self, sensor, sensor_index, mc, length=1000):
        self.__sensor = sensor
        self.__sensor_index = sensor_index
        self.__mc = mc
        self.__length = 1000
        self.bounds = []

    def homing(self):
        self.__mc.rotate(0, 10000)
        distance = self.__sensor.distance(self.__sensor_index)
        while((0.1 * self.__length) < distance < (0.9 * self.__length)):
            distance = self.__sensor.distance(self.__sensor_index)
            #print(distance)
        self.__mc.stop(0)
        position = self.__mc.position(0)
        self.bounds.append((distance, position))
        self.__mc.rotate(0, -10000)
        if((0.05 * self.__length) < distance < (0.15 * self.__length)): # lower
            while(distance < (0.9 * self.__length)):
                distance = self.__sensor.distance(self.__sensor_index)
        else: # higher
            while((0.1 * self.__length) < distance):
                distance = self.__sensor.distance(self.__sensor_index)
        self.__mc.stop(0)
        position = self.__mc.position(0)
        self.bounds.append((distance, position))
