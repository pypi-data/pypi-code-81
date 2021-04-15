# -*- coding: UTF-8 -*-

from threading import Thread, BoundedSemaphore as IthreadBoundedSemaphore


class Ithread(Thread):
    def __init__(self, func, args):
        Thread.__init__(self)
        self.func = func
        self.args = args

    def getResult(self):
        return self.result

    def run(self):
        self.result = self.func(*self.args)


class RestoreNesting(object):
    outdict = {}

    def __init__(self):
        self.outdict = {}

    #将多层嵌套的dict，解包为单层，key相加。
    def nested_dict(self, indict, parentkey=''):
        for key in indict:
            if isinstance(indict[key], dict):
                self.nested_dict(indict[key], parentkey + str(key) + '-')
            else:
                self.outdict[parentkey + str(key)] = indict[key]
        return self.outdict