__all__ = ["PyModuleTestCase"]
import os
import sys
import unittest
from test.utils import *


class PyModuleTestCase(TestCaseBase):
    def test_hello(self):
        """This node has an implicit configured module."""
        stdout, stderr = self.call(
            ["testnodes.pymodule_hello", "john"], has_stdout=True, has_stderr=False
        )

        self.assertEqual(stdout, "hello john !", "wrong output")

    def test_hello2(self):
        """This node has an explicit configured module."""
        stdout, stderr = self.call(
            ["testnodes.pymodule_hello2", "john"], has_stdout=True, has_stderr=False
        )

        self.assertEqual(stdout, "hello john !", "wrong output")

    def test_hello_stderr(self):
        """Test calling pymodule_hello without arguments => print argparse help."""
        stdout, stderr = self.call(
            ["testnodes.pymodule_hello"], has_stdout=False, has_stderr=True
        )

        self.assertIn("usage: hello [-h]", stderr, "wrong output")

    def test_noentrypoint(self):
        """This node has no configured entrypoint."""
        stdout, stderr = self.call(
            ["testnodes.pymodule_noentrypoint"], has_stdout=False, has_stderr=True
        )

        self.assertIn("missing entrypoint in configuration", stderr, "wrong output")

    def test_invalidmodule(self):
        """This node has an invalid configured module."""
        stdout, stderr = self.call(
            ["testnodes.pymodule_invalidmodule"], has_stdout=False, has_stderr=True
        )

        self.assertIn("failed to import module invalid", stderr, "wrong output")

    def test_invalidentrypoint(self):
        """This node has an invalid configured entrypoint."""
        stdout, stderr = self.call(
            ["testnodes.pymodule_invalidentrypoint"], has_stdout=False, has_stderr=True
        )

        self.assertIn(
            "module testnodes has no entrypoint invalid",
            stderr,
            "wrong output",
        )


if __name__ == "__main__":
    unittest.main()
