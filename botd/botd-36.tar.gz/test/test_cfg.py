# This file is placed in the Public Domain.

import unittest

from botl.edt import edit
from botl.prs import parseargs

from test.run import t

class Test_Cfg(unittest.TestCase):

    def test_parse(self):
        parseargs(t.cfg, "mods=irc")
        self.assertEqual(t.cfg.sets.mods, "irc")

    def test_parse2(self):
        parseargs(t.cfg, "mods=csl")
        self.assertEqual(t.cfg.sets.mods, "csl")

    def test_edit(self):
        d = {"mods": "csl"}
        edit(t.cfg, d)
        self.assertEqual(t.cfg.mods, "csl")
