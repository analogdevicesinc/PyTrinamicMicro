from PyTrinamicMicro.platforms.motionpy1.modules.MCP23S08 import MCP23S08
from pyb import Pin
from pyb import Timer
import time

class hc_sr04_multi(object):

    def __init__(self, cs=Pin.cpu.A4, trigger=Pin.cpu.C0, echo=Pin.cpu.C1, timer=Timer(2), avg_window=1):
        self.__io = MCP23S08(cs=cs)
        self.__trigger = Pin(trigger, Pin.OUT_PP)
        self.__echo = Pin(echo, Pin.IN, pull=Pin.PULL_DOWN)
        self.__timer = timer
        self.__counter = 0
        self.__window_len = avg_window
        self.__window = []

        self.__trigger.high()
        self.__io.set_direction(0, 0)
        self.__io.set_direction(1, 0)
        self.__io.set_direction(2, 0)
        self.__io.set_direction(3, 0)
        self.__io.set_gpio(0, 0)
        self.__io.set_gpio(1, 0)
        self.__io.set_gpio(2, 0)
        self.__io.set_gpio(3, 0)

        self.select_sensor(3)

    def __echo_rising(self, p):
        self.__timer.counter(0)
        self.__echo.irq(handler=self.__echo_falling, trigger=Pin.IRQ_FALLING)
        #print(self.__distance((self.__counter * 20) / 65537))
        #exit()

    def __echo_falling(self, p):
        #print("echo {}".format(self.__timer.counter()))
        self.__counter = self.__timer.counter()
        self.__echo.irq(trigger=0)

    def __timeout(self, t):
        t.deinit()
        #print("timeout")
        self.__counter = 16800000

    def select_sensor(self, sensor):
        self.__io.set_gpio(0, 0)
        self.__io.set_gpio(1, 0)
        self.__io.set_gpio(2, 0)
        self.__io.set_gpio(3, 0)
        self.__io.set_gpio(sensor, 1)

    def duration(self, sensor):
        self.select_sensor(sensor)
        #time.sleep(20E-6)
        #print("Trigger: {}, Echo: {}".format(self.__trigger.value(), self.__echo.value()))
        #while(True):
        #    pass
        self.__counter = 16800000
        while(self.__counter == 16800000):
            self.__counter = 0
            self.__trigger.low()
            time.sleep(3E-6)
            self.__trigger.high()
            time.sleep(20E-6)
            self.__trigger.low()
            self.__echo.irq(handler=self.__echo_rising, trigger=Pin.IRQ_RISING)
            time.sleep(450E-6)
            self.__timer.init(prescaler=0, period=16800000, callback=self.__timeout)
            self.__timer.counter(0)
            #self.__timer.init(freq=)
            while(self.__counter == 0):
                pass
            self.__timer.deinit()
            #self.__echo.irq(trigger=0)
        return (self.__counter * 0.2) / 16800 # ms

    def __distance(self, duration, temp_deg=20):
        return (duration * (331.5 + (0.6 * temp_deg))) / 2 # mm

    def distance(self, sensor, temp_deg=20):
        distance = self.__distance(self.duration(sensor), temp_deg)
        self.__window.insert(0, distance)
        self.__window = self.__window[0:self.__window_len]
        return (sum(self.__window) / len(self.__window))
