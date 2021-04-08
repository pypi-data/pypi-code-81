# This file is placed in the Public Domain.

"test all commands sequentialy"

from botl.evt import Command
from botl.krn import kernel
from botl.utl import cprint
from botl.zzz import time, unittest
from test.prm import param
from test.run import t

k = kernel()

class Test_Cmd(unittest.TestCase):

    def test_cmds(self):
        for x in range(k.cfg.index or 1):
            for cmd in k.modnames:
                exec(cmd)

def exec(cmd):
    exs = getattr(param, cmd, [""])
    for ex in list(exs):
        txt = cmd + " " + ex
        e = Command({"txt": txt, "orig": repr(t)})
        cprint(txt)
        k.put(e)
