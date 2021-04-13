# This file is placed in the Public Domain.

"test objects"

from op.obj import O, Object, default
from op.zzz import json, unittest

class Test_JSON(unittest.TestCase):

    def test_jsonO(self):
        o = O()
        o.test = "bla"
        v = json.dumps(o, default=default)
        self.assertTrue(str(o) == v)

    def test_jsonObject(self):
        o = Object()
        o.test = "bla"
        v = json.dumps(o, default=default)
        self.assertEqual(str(o), v)

    def test_jsonreconstructO(self):
        o = O()
        o.test = "bla"
        v = json.dumps(o, default=default)
        vv = json.loads(v, object_hook=O)
        self.assertEqual(str(o), str(vv))

    def test_jsonreconstruvtObject(self):
        o = Object()
        o.test = "bla"
        v = json.dumps(o, default=default)
        vv = json.loads(v, object_hook=Object)
        self.assertEqual(str(o), str(vv))
    