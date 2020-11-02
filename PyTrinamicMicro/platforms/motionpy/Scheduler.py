'''
Scheduler class to schedule tasks.

Created on 29.10.2020

@author: LK
'''

import logging
from pyb import RTC

class SchedulerStatus(object):
    pass

class SchedulerStatusStopped(SchedulerStatus):
    def __str__(self):
        return "Stopped"

class SchedulerStatusRunning(SchedulerStatus):
    def __str__(self):
        return "Running"


class Scheduler(object):

    def __init__(self, interval=1000):
        self.__interval = interval
        self.__tasks = []
        self.__status = SchedulerStatusStopped()
        self.__logger = logging.getLogger(self.__module__)

    @staticmethod
    def __is_zero(datetime):
        if(not(datetime)):
            return True
        for i in range(0, len(datetime)):
            if(datetime[i] != 0):
                return False
        return True

    @staticmethod
    def __add_dates(first, second):
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
        for task in self.__tasks:
            if(self.__due(task["datetime"], current)):
                self.__logger.debug("Task {} is due. Executing ...".format(task["id"]))
                task["function"](*task["args"], **task["kwargs"])
                if(self.__is_zero(task["interval"])):
                    self.__tasks.remove(task)
                else:
                    task["datetime"] = self.__add_dates(current, task["interval"])

    def start(self):
        RTC().wakeup(self.__interval, self.__tick)
        self.__status = SchedulerStatusRunning()
        self.__logger.debug("Scheduler {} started.".format(self))

    def stop(self):
        RTC().wakeup(None)
        self.__status = SchedulerStatusStopped()
        self.__logger.debug("Scheduler {} stopped.".format(self))

    def status(self):
        return self.__status

    def register_task(self, id, datetime, interval, func, *args, **kwargs):
        self.__tasks.append({
            "id": id,
            "datetime": datetime,
            "interval": interval,
            "function": func,
            "args": args,
            "kwargs": kwargs
        })

    def remove_task(self, id):
        self.__tasks = [e for e in self.__tasks if e["id"] != id]
