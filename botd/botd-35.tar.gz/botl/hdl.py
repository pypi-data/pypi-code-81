# This file is placed in the Public Domain.

"handler"

from .bus import Bus
from .obj import Object
from .thr import launch
from .trc import exception
from .utl import locked
from .zzz import queue, time, _thread

class Handler(Object):

    def __init__(self):
        super().__init__()
        self.cbs = Object()
        self.queue = queue.Queue()
        self.stopped = False

    def addbus(self):
        Bus.add(self)

    def callbacks(self, event):
        try:
            self.cbs[event.type](self, event)
        except KeyError:
            event.ready()
        except Exception as ex:
            print(exception())
            event.ready()

    def handler(self):
        while not self.stopped:
            e = self.queue.get()
            if self.stopped:
                break
            self.callbacks(e)

    def put(self, e):
        self.queue.put_nowait(e)

    def register(self, name, callback):
        self.cbs[name] = callback

    def start(self):
        self.stopped = False
        launch(self.handler)
        return self

    def stop(self):
        self.stopped = True
        self.queue.put(None)

def cmd(hdl, obj):
    obj.parse()
    f = hdl.cmd(obj.cmd)
    res = None
    if f:
        res = f(obj)
        obj.show()
    obj.ready()
    return res
