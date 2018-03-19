#coding:utf_8

from utils.commons import elaspe_timer, RunningTimer

class BaseModel(object):

    def __init__(self):
        pass

    @staticmethod
    @elaspe_timer
    def search():
        return {"data":{"row":1}}

    