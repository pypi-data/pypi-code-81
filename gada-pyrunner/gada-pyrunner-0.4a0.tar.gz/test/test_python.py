__all__ = ["PythonTestCase"]
import os
import sys
import io
import unittest
from test.utils import *


class PythonTestCase(TestCaseBase):
    def test_hello(self):
        """Test calling python_hello with argument."""
        stdout, stderr = self.call(
            ["testnodes.python_hello", "john"], has_stdout=True, has_stderr=False
        )

        self.assertEqual(stdout, "hello john !", "wrong output")

    def test_hello_stderr(self):
        """Test calling python_hello without arguments => print argparse help."""
        stdout, stderr = self.call(
            ["testnodes.python_hello"], has_stdout=False, has_stderr=True
        )

        self.assertIn("usage: hello [-h]", stderr, "wrong output")


if __name__ == "__main__":
    unittest.main()
