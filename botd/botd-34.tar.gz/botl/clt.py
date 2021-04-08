# This file is in the Public Domain.

"clients"

from .bus import Bus
from .err import ENOTIMPLEMENTED
from .evt import Command
from .krn import kernel
from .hdl import Handler, cmd
from .obj import Object
from .thr import launch
from .utl import cprint
from .zzz import queue, threading

verbose = False

class Client(Handler):

    def __init__(self):
        super().__init__()
        self.iqueue = queue.Queue()
        
    def announce(self, txt):
        pass

    def dosay(self, channel, txt):
        cprint(txt)

    def event(self, txt):
        return Command({"txt": txt, "orig": repr(self)})

    def input(self):
        k = kernel()
        while not self.stopped:
            e = self.once()
            if self.stopped:
                break
            self.put(e)

    def once(self):
        return self.event(self.poll()).parse()

    def poll(self):
        return self.iqueue.get()

    def reconnect(self):
        pass

    def start(self):
        super().start()
        launch(self.input)

    def stop(self):
        self.stopped = True
        self.iqueue.put_nowait("")

    def wait(self):
        self.connected.wait()

class CLI(Client):

    def dosay(self, channel, txt):
        if not self.stopped:
            print(txt)

    def input(self):
        k = kernel()
        while not self.stopped:
            e = self.once()
            if self.stopped:
                break
            k.put(e)
            e.wait()

class Test(CLI):

    def dosay(self, channel, txt):
        k = kernel()
        if k.cfg.verbose:
            print(txt)

def run(hdl, txt):
    k = kernel()
    c = CLI()
    c.addbus()
    c.start()
    e = Command({"txt": txt, "orig": repr(c)})
    cmd(k, e)
    e.wait()
