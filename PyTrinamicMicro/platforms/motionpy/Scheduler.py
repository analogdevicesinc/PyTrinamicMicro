'''
Scheduler class to schedule tasks.

Created on 29.10.2020

@author: LK
'''

from pyb import RTC

class Scheduler(object):

    def __init__(self, interval=1000):
        self.tasks = []
        RTC().wakeup(interval, self.__tick)

    @staticmethod
    def __is_zero(datetime):
        if(not(datetime)):
            return True
        for i in range(0, len(datetime)):
            if(datetime[i] != 0):
                return False
        return True

    @staticmethod
    def add_dates(first, second):
        first = list(first)
        for i in range(0, len(second)):
            first[i] = first[i] + second[i]
        return tuple(first)

    @staticmethod
    def __due(config, current):
        for i in range(0, len(config)):
            if(current[i] < config[i]):
                return False
            if(current[i] > config[i]):
                return True
        return True

    def __tick(self, arg):
        current = RTC().datetime()
        for task in self.tasks:
            print("current: {}, task: {}".format(current, task["datetime"]))
            if(self.__due(task["datetime"], current)):
                task["function"](*task["args"], **task["kwargs"])
                if(self.__is_zero(task["interval"])):
                    self.tasks.remove(task)
                else:
                    task["datetime"] = self.__add_dates(task["datetime"], task["interval"])

    def stop(self):
        RTC().wakeup(None)

    def register_task(self, datetime, interval, func, *args, **kwargs):
        self.tasks.append({
            "datetime": datetime,
            "interval": interval,
            "function": func,
            "args": args,
            "kwargs": kwargs
        })
