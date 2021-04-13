import unittest
from palaestrai.core import RuntimeConfig


class RuntimeConfigTestCase(unittest.TestCase):
    def test_singleton(self):
        self.assertEqual(id(RuntimeConfig()), id(RuntimeConfig()))

    def test_implicit_load(self):
        c = RuntimeConfig()
        self.assertTrue(c._conf_dict)

    def test_load_from_file(self):
        c = RuntimeConfig()
        self.assertTrue(c._config_file_path)
        c.load("./arl-runtime.conf.yaml")
        self.assertTrue(c._config_file_path)
        self.assertEqual(c._config_file_path, "./arl-runtime.conf.yaml")

    def test_load_from_stream(self):
        from io import StringIO

        store_ui = "psql://foo:bar@baz.example.com/meeple"
        stream = StringIO("store_uri: %s" % store_ui)
        RuntimeConfig().load(stream)
        self.assertEqual(RuntimeConfig().store_uri, store_ui)


if __name__ == "__main__":
    unittest.main()
