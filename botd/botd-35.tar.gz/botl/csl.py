# This file is in the Public Domain.

"console"

from .clt import CLI, cmd

def init(hdl):
    c = Console()
    c.addbus()
    c.start()
    return c

class Console(CLI):

    def __init__(self):
        super().__init__()
        self.register("cmd", cmd)

    def dosay(self, channel, txt):
        print(txt)

    def poll(self):
        return input("> ")
