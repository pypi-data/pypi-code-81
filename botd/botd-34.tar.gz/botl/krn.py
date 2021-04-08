# This file is placed in the Public Domain.

"kernel"

__version__ = 1

from .bus import Bus
from .dbs import last
from .evt import Command
from .hdl import Handler, cmd
from .itr import findcmds, hasmod
from .itr import scan as iscan
from .itr import walk as iwalk
from .obj import Cfg, Default, Object, ObjectList, cdir, fmt, save
from .prs import parse as myparse
from .thr import launch
from .trm import termreset, termsave
from .utl import cprint, direct, op, spl
from .zzz import os, queue, shutil, sys, time, _thread

kernels = []
starttime = time.time()

class Cfg(Cfg):

    def __init__(self, val=None):
        super().__init__()
        self.name = "botl"
        self.users = True
        self.version = __version__
        self.verbose = False
        if val:
            self.update(val)

class Kernel(Handler):

    cmds = Object()
    pnames = Object()
    modnames = Object()
    names = ObjectList()
    table = Object()

    def __init__(self, tbl=None, **kwargs):
        super().__init__()
        self.cfg = Cfg()
        self.register("cmd", cmd)
        if not tbl:
            try:
                from botl.tbl import tbl
            except ImportError:
                pass
        self.tbl(tbl)
        if not kernels:
            kernels.append(self)

    def add(self, name, cmd):
        self.cmds.register(name, cmd)
        Kernel.modnames[name] = cmd.__module__

    def announce(self, txt):
        pass

    def banner(self):
        cprint("%s %s started at %s" % (self.cfg.name.upper(), __version__, time.ctime(time.time())))
        cprint(fmt(self.cfg, skip=["old", "txt"]))

    def cmd(self, cmd):
        if cmd not in self.cmds:
            mn = self.modname(cmd)
            if mn:
                self.load(mn)
        return self.cmds.get(cmd, None)

    def debug(self):
        import botl.url
        botl.url.debug = True

    def dosay(self, channel, txt):
        pass

    def hup(self):
        for b in Bus.objs:
            if "cfg" in b:
                last(b.cfg)

    def init(self, mns):
        for mn in spl(mns):
            mnn = self.name(mn)
            if mnn and hasmod(mnn):
                mod = self.load(mnn)
                if mod and "init" in dir(mod):
                    mod.init(self)

    def loader(self, mns):
        for mn in spl(mns):
            mnn = self.name(mn)
            if mnn:
                mod = self.load(mnn)

    def load(self, mnn):
        if mnn in Kernel.table:
            return Kernel.table[mnn]
        mod = direct(mnn)
        cmds = findcmds(mod)
        self.cmds.update(cmds)
        Kernel.table[mnn] = mod
        return mod

    def name(self, mn):
        return Kernel.pnames.get(mn, None)

    def modname(self, mn):
        return Kernel.modnames.get(mn, None)

    def parse(self, wd=None):
        import botl.obj
        myparse(self.cfg, " ".join(sys.argv[1:]))
        self.cfg.update(self.cfg.sets or {})
        if op("v"):
           self.cfg.verbose = True
        botl.obj.wd = self.cfg.wd = wd or self.cfg.wd or os.path.expanduser("~/.%s" % self.cfg.name)
        return self.cfg

    def rmdir(self, path):
        if os.path.exists(path):
            shutil.rmtree(path)

    def run(self, txt=None):
        if not txt and not self.cfg.txt:
            return
        txt = txt or self.cfg.old.txt
        from .clt import CLI
        c = CLI()
        c.addbus()
        c.start()
        e = Command({"txt": txt, "orig": repr(c)})
        cmd(self, e)
        e.wait()
        _thread.interrupt_main()

    def scan(self, path, name=""):
        if not os.path.exists(path):
            return
        if not name:
            name = path.split(os.sep)[-1]
        r = os.path.dirname(path)
        sys.path.insert(0, r)
        for mn in [x[:-3] for x in os.listdir(path)
                   if x and x.endswith(".py")
                   and not x.startswith("__")
                   and not x == "setup.py"]:
            fqn = "%s.%s" % (name, mn)
            mod = self.load(fqn)
            iscan(self, mod)

    def tbl(self, tbl):
        Kernel.names = ObjectList()
        Kernel.names.update(tbl["names"])
        Kernel.modnames.update(tbl["modnames"])
        Kernel.pnames.update(tbl["pnames"])

    def types(self, typ):
        return list(Kernel.names.get(typ, [typ,]))

    def walk(self, pkgs):
        tbl = iwalk(pkgs)
        self.tbl(tbl)
        
    def wait(self, timeout=None):
        while not self.stopped:
            time.sleep(timeout or 30.0)

def exec(main):
    termsave()
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        termreset()

def kernel():
    if kernels:
        return kernels[0]

def op(ops):
    k = kernel()
    for opt in ops:
        if opt in k.cfg.opts:
            return True
    return False
