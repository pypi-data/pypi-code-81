# This file is placed in the Public Domain.

import unittest

from op.edt import edit
from op.prs import parseargs

from test.run import t

class Test_Cfg(unittest.TestCase):

    def test_parse(self):
        parseargs(t.cfg, "mods=irc")
        self.assertEqual(t.cfg.sets.mods, "irc")

    def test_parse2(self):
        parseargs(t.cfg, "mods=udp")
        self.assertEqual(t.cfg.sets.mods, "udp")

    def test_edit(self):
        d = {"mods": "rss"}
        edit(t.cfg, d)
        self.assertEqual(t.cfg.mods, "rss")
