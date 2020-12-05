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

    def homing(self, velocity=10000, margin=0.1, margin_hyst=0.5):
        self.bounds = []
        self.__mc.rotate(0, velocity)
        distance = self.__sensor.distance(self.__sensor_index)
        while((margin * self.__length) < distance < ((1.0 - margin) * self.__length)):
            distance = self.__sensor.distance(self.__sensor_index)
            #print(distance)
        self.__mc.stop(0)
        position = self.__mc.position(0)
        self.bounds.append((distance, position))
        self.__mc.rotate(0, -velocity)
        if(((margin - (margin * margin_hyst)) * self.__length) < distance < ((margin + (margin * margin_hyst)) * self.__length)): # lower
            while(distance < ((1.0 - margin) * self.__length)):
                distance = self.__sensor.distance(self.__sensor_index)
        else: # higher
            while((margin * self.__length) < distance):
                distance = self.__sensor.distance(self.__sensor_index)
        self.__mc.stop(0)
        position = self.__mc.position(0)
        self.bounds.append((distance, position))
        self.bounds.sort(key=lambda x: x[0])

    def position(self, position, acceleration=1000, velocity=100000):
        if(not(self.bounds)):
            raise ValueError("Run homing sequence first.")

        position = int(self.bounds[0][1] + ((self.bounds[1][1] - self.bounds[0][1]) * position))

        self.__mc.velocity(0, velocity)
        self.__mc.acceleration(0, acceleration)
        self.__mc.moveTo(0, position, 0)
