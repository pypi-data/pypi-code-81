# This file is in the Public Domain.

"administrator"

from .bus import Bus
from .dbs import last
from .edt import edit
from .krn import kernel, starttime, __version__
from .obj import Object, fmt, getname, save
from .tms import elapsed
from .trc import exc as iexc
from .zzz import threading, time

k = kernel()

def exc(event):
    if iexc:
        event.reply("|".join(iexc))

def flt(event):
    try:
        index = int(event.args[0])
        event.reply(str(Bus.objs[index]))
        return
    except (TypeError, IndexError):
        pass
    event.reply(" | ".join([getname(o) for o in Bus.objs]))

def krn(event):
    k = kernel()
    if not event.sets:
        event.reply(fmt(k.cfg, skip=["opts", "sets", "old", "res"]))
        return
    edit(k.cfg, event.sets)
    save(k.cfg)
    event.reply("ok")

def sve(event):
    save(k)
    event.reply("ok")

def thr(event):
    psformat = "%s %s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        o = Object()
        o.update(vars(thr))
        if getattr(o, "sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - starttime)
        thrname = thr.getName()
        if not thrname:
            continue
        if thrname:
            result.append((up, thrname))
    res = []
    for up, txt in sorted(result, key=lambda x: x[0]):
        res.append("%s %s" % (txt, elapsed(up)))
    if res:
        event.reply(" | ".join(res))

def upt(event):
    event.reply("uptime is %s" % elapsed(time.time()-starttime))

def ver(event):
    k = kernel()
    event.reply("%s %s" % (k.cfg.name.upper(), k.cfg.version or __version__))

"""def vrb(event):
    k = kernel()
    if not k.cfg.verbose:
        k.cfg.verbose = True
        save(k.cfg)
        event.reply("verbose is on")
    else:
        k.cfg.verbose = False
        save(k.cfg)
        event.reply("verbose is off")
"""