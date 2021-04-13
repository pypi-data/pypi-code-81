# This file is placed in the Public Domain.

from op.bus import Bus
from op.evt import Command, events
from op.obj import fmt
from op.thr import launch
from op.utl import cprint
from op.zzz import random, unittest

from test.prm import param
from test.run import t

class Test_Threaded(unittest.TestCase):

    def test_thrs(self):
        thrs = []
        for x in range(t.cfg.index or 1):
            thr = launch(exec)
            thrs.append(thr)
        for thr in thrs:
            thr.join()
        consume()
        #t.stop()

def consume():
    fixed = []
    res = []
    for e in events:
        e.wait()
        fixed.append(e)
    for f in fixed:
        try:
            events.remove(f)
        except ValueError:
            continue
    return res

def exec():
    l = list(t.modnames)
    random.shuffle(l)
    for cmd in l:
        if cmd not in param:
            cprint(cmd)
            e = Command({"txt": cmd, "orig": repr(t)})
            t.put(e)
            events.append(e)
            continue
        for ex in getattr(param, cmd, [""]):
            txt = cmd + " " + ex
            cprint(txt)
            e = Command({"txt": txt, "orig": repr(t)})
            t.put(e)
            events.append(e)
