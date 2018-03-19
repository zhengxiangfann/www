#encoding: utf-8

import logging
import inspect
import time

def elaspe_timer(func):
    def new_func(*args, **argsx):
        start_time = time.time()
        ret = func(*args, **argsx)
        etime = time.time() - start_time
        msg = "[%s.%s] Time consumed: %s seconds" % (func.__class__.__name__, func.__name__, etime)
        logging.getLogger(msg)
        print(msg)
        return ret
    return new_func

class RunningTimer(object):
    def __init__(self):
        self.__start_time = time.time()
        self.__last_time = self.__start_time

    def consumed(self):
        cur_time = time.time()
        consumed_time = time.time() - self.__last_time
        self.__last_time = cur_time
        return consumed_time

    def total_consumed(self):
        return time.time() - self.__start_time