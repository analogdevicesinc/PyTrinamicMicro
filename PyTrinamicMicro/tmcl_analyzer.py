'''
Created on 05.02.2021

@author: LK
'''

from PyTrinamicMicro.connections.tmcl_host_interface import tmcl_host_interface
from PyTrinamicMicro.connections.tmcl_module_interface import tmcl_module_interface
from PyTrinamic.TMCL import TMCL, TMCL_Request, TMCL_Reply
import logging
import time

class tmcl_analyzer(object):

    def __init__(self, connection_host=None, connection_module=None, callback_request=None, callback_reply=None, measure_window=None):
        self.__connection_host = connection_host
        self.__connection_module = connection_module
        self.__callback_request = callback_request
        self.__callback_reply = callback_reply
        self.__measure_window = measure_window
        self.__logger = logging.getLogger(self.__module__)

        self.__measure_start = 0
        self.__measure_count = 0
        self.__throughput = 0
        self.__wait = False

    def process(self):
        if(self.__connection_host):
            if(self.__connection_host.request_available() and not(self.__wait)):
                request = self.__connection_host.receive_request()
                if(self.__callback_request):
                    self.__callback_request(request)
                if(self.__measure_window):
                    self.__measure_count += 1
                if(self.__connection_module):
                    self.__wait = True
        if(self.__connection_module):
            if(self.__connection_module.reply_available() and self.__wait):
                reply = self.__connection_module.receive_reply()
                if(self.__callback_reply):
                    self.__callback_reply(reply)
                if(not(self.__connection_host)):
                    self.__measure_count += 1
                self.__wait = False
        if(self.__measure_window):
            t = time.time()
            if(t - self.__measure_start > self.__measure_window):
                self.__throughput = self.__measure_count / (t - self.__measure_start)
                self.__measure_start = t
                self.__measure_count = 0

    def throughput(self):
        return self.__throughput
