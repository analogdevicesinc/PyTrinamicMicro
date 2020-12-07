from PyTrinamic.ic.TMC5130.TMC5130 import TMC5130
from PyTrinamicMicro.platforms.motionpy.connections.uart_ic_interface import uart_ic_interface
from PyTrinamicMicro.platforms.motionpy.modules.hc_sr04_multi import hc_sr04_multi
from PyTrinamicMicro.platforms.motionpy.modules.MCP23S08 import MCP23S08
from PyTrinamic.modules.TMCM0960.TMCM0960 import TMCM0960
import logging

class linear_distance(object):

    def __init__(self, sensor, sensor_index, mc, length=1000):
        self.__sensor = sensor
        self.__sensor_index = sensor_index
        self.mc = mc
        self.__length = 1000
        self.bounds = []

    def homing_direct(self, velocity=10000, margin=0.1, margin_hyst=0.5):
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

    def homing(self, homing_status, length=1000, velocity=10000, acceleration=1000, margin=0.1, margin_hyst=0.5):
        if(homing_status == TMCM0960.ENUMs.HOMING_STATUS_INIT):
            self.bounds = []
            #print(velocity)
            self.mc.writeRegister(self.mc.registers.AMAX, acceleration)
            self.mc.writeRegister(self.mc.registers.A1, acceleration)
            self.mc.writeRegister(self.mc.registers.DMAX, acceleration)
            self.mc.writeRegister(self.mc.registers.D1, acceleration)
            self.mc.rotate(0, velocity)
            homing_status = TMCM0960.ENUMs.HOMING_STATUS_FIRST
        elif(homing_status == TMCM0960.ENUMs.HOMING_STATUS_FIRST):
            distance = self.__sensor.distance(self.__sensor_index)
            if(((margin * length) > distance) or (distance > ((1.0 - margin) * length))):
                self.bounds.append((distance, self.mc.readRegister(self.mc.registers.XACTUAL, signed=True)))
                self.mc.rotate(0, -velocity)
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
                self.bounds.append((distance, self.mc.readRegister(self.mc.registers.XACTUAL, signed=True)))
                self.mc.stop(0)
                self.bounds.sort(key=lambda x: x[0])
                homing_status = TMCM0960.ENUMs.HOMING_STATUS_DONE
        return homing_status

    def position_step(self, position=None, velocity=10000, acceleration=1000):
        if(position is None):
            return self.mc.readRegister(self.mc.registers.XACTUAL, signed=True)
        else:
            self.mc.writeRegister(self.mc.registers.VMAX, velocity)
            self.mc.writeRegister(self.mc.registers.VSTART, velocity)
            self.mc.writeRegister(self.mc.registers.V1, velocity)
            self.mc.writeRegister(self.mc.registers.VSTOP, velocity)
            self.mc.writeRegister(self.mc.registers.AMAX, acceleration)
            self.mc.writeRegister(self.mc.registers.A1, acceleration)
            self.mc.writeRegister(self.mc.registers.DMAX, acceleration)
            self.mc.writeRegister(self.mc.registers.D1, acceleration)
            self.mc.moveTo(0, position)

    def position_absolute(self, position=None, velocity=10000, acceleration=1000):
        if(position is None):
            return self.__sensor.distance(self.__sensor_index)
        else:
            self.position_step(int(self.bounds[0][0] + (((self.bounds[1][1] - self.bounds[0][1]) * (position - self.bounds[0][0])) / (self.bounds[1][0] - self.bounds[0][0]))),
                velocity, acceleration)

    def position_relative(self, position=None, velocity=None, acceleration=None):
        if(position is None):
            return ((self.position_absolute() - self.bounds[0][0]) / (self.bounds[1][0] - self.bounds[0][0]))
        else:
            self.position_step(int(self.bounds[0][1] + ((self.bounds[1][1] - self.bounds[0][1]) * position)),
                velocity, acceleration)
