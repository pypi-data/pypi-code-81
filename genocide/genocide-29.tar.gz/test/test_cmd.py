# This file is placed in the Public Domain.

"test all commands sequentialy"

from op.evt import Command
from op.utl import cprint
from op.zzz import time, unittest

from test.prm import param
from test.run import t

class Test_Cmd(unittest.TestCase):

    def test_cmds(self):
        for x in range(t.cfg.index or 1):
            for cmd in t.modnames:
                exec(cmd)

def exec(cmd):
    exs = getattr(param, cmd, [""])
    for ex in list(exs):
        txt = cmd + " " + ex
        e = Command({"txt": txt, "orig": repr(t)})
        cprint(txt)
        t.put(e)
