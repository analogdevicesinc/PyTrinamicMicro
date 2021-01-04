from PyTrinamicMicro.platforms.motionpy.modules.hc_sr04_multi import hc_sr04_multi
from PyTrinamicMicro.platforms.motionpy.modules.MCP23S08 import MCP23S08
from PyTrinamic.modules.TMCM0960.TMCM0960 import TMCM0960
import logging

class linear_distance(object):

    def __init__(self, sensor, sensor_index, module, length=1000):
        self.__sensor = sensor
        self.__sensor_index = sensor_index
        self.module = module
        self.__length = 1000
        self.bounds = []

    def homing_direct(self, velocity=10000, margin=0.2, margin_hyst=0.5):
        self.bounds = []
        self.module.rotate(0, velocity)
        distance = self.__sensor.distance(self.__sensor_index)
        while((margin * self.__length) < distance < ((1.0 - margin) * self.__length)):
            distance = self.__sensor.distance(self.__sensor_index)
            print(distance)
        self.module.stop(0)
        position = self.module.getActualPosition(0)
        self.bounds.append((distance, position))
        self.module.rotate(0, -velocity)
        if(((margin - (margin * margin_hyst)) * self.__length) < distance < ((margin + (margin * margin_hyst)) * self.__length)): # lower
            while(distance < ((1.0 - margin) * self.__length)):
                distance = self.__sensor.distance(self.__sensor_index)
                print(distance)
        else: # higher
            while((margin * self.__length) < distance):
                distance = self.__sensor.distance(self.__sensor_index)
                print(distance)
        self.module.stop(0)
        position = self.module.getActualPosition(0)
        self.bounds.append((distance, position))
        self.bounds.sort(key=lambda x: x[0])

    def homing(self, homing_status, length=1000, velocity=10000, acceleration=1000, margin=0.2, margin_hyst=0.5):
        if(homing_status == TMCM0960.ENUMs.HOMING_STATUS_INIT):
            self.bounds = []
            #print(velocity)
            self.module.setMaxAcceleration(0, acceleration)
            self.module.rotate(0, velocity)
            homing_status = TMCM0960.ENUMs.HOMING_STATUS_FIRST
        elif(homing_status == TMCM0960.ENUMs.HOMING_STATUS_FIRST):
            distance = self.__sensor.distance(self.__sensor_index)
            if(((margin * length) > distance) or (distance > ((1.0 - margin) * length))):
                self.bounds.append((distance, self.module.getActualPosition(0)))
                self.module.rotate(0, -velocity)
                homing_status = TMCM0960.ENUMs.HOMING_STATUS_SECOND
        elif(homing_status == TMCM0960.ENUMs.HOMING_STATUS_SECOND):
            distance = self.__sensor.distance(self.__sensor_index)
            #print("distance: {}, bounds[0][0]: {}, margin: {}, hyst: {}".format(distance, self.bounds[0][0], margin, margin_hyst))
            done = False
            if(self.bounds[0][0] < ((margin + (margin * margin_hyst)) * length)): # lower
                done = (distance > ((1.0 - margin) * length))
            else: # higher
                done = ((margin * length) > distance)
            if(done):
                self.bounds.append((distance, self.module.getActualPosition(0)))
                self.module.stop(0)
                self.bounds.sort(key=lambda x: x[0])
                homing_status = TMCM0960.ENUMs.HOMING_STATUS_DONE
        return homing_status

    def position_step(self, position=None, velocity=10000, acceleration=1000):
        if(position is None):
            return self.module.getActualPosition(0)
        else:
            self.module.setMaxAcceleration(0, acceleration)
            self.module.setMaxVelocity(0, velocity)
            self.module.moveTo(0, position)

    def position_absolute(self, position=None, velocity=10000, acceleration=1000):
        if(position is None):
            return self.__sensor.distance(self.__sensor_index)
        else:
            self.position_step(int((((position - self.bounds[0][0]) * (self.bounds[1][1] - self.bounds[0][1])) / (self.bounds[1][0] - self.bounds[0][0])) + self.bounds[0][1]),
                velocity, acceleration)

    def position_relative(self, position=None, velocity=None, acceleration=None):
        if(position is None):
            return ((self.position_absolute() - self.bounds[0][0]) / (self.bounds[1][0] - self.bounds[0][0]))
        else:
            self.position_step(int(self.bounds[0][1] + ((self.bounds[1][1] - self.bounds[0][1]) * position)),
                velocity, acceleration)
