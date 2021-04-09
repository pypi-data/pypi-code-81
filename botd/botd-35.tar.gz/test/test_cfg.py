# This file is placed in the Public Domain.

import unittest

from botl.edt import edit
from botl.krn import kernel
from botl.prs import parse

k = kernel()

class Test_Cfg(unittest.TestCase):

    def test_parse(self):
        parse(k.cfg, "mods=irc")
        self.assertEqual(k.cfg.sets.mods, "irc")

    def test_parse2(self):
        parse(k.cfg, "mods=csl")
        self.assertEqual(k.cfg.sets.mods, "csl")

    def test_edit(self):
        d = {"mods": "csl"}
        edit(k.cfg, d)
        self.assertEqual(k.cfg.mods, "csl")
