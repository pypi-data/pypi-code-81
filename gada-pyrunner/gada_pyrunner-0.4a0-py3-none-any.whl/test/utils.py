# -*- coding: utf-8 -*-
from __future__ import annotations
import os
import subprocess
import yaml
import unittest
import gada.test_utils
import gada_pyrunner


def _run(argv: Optional[list[str]] = None) -> tuple[str, str]:
    argv = argv if argv is not None else []

    with gada.test_utils.PipeStream() as stdin:
        stdin.writer.close()

        with gada.test_utils.PipeStream(rmode="r", wmode="w") as stdout:
            with gada.test_utils.PipeStream(rmode="r", wmode="w") as stderr:
                proc = subprocess.Popen(
                    ["gada"] + argv, stdout=stdout.writer, stderr=stderr.writer
                )
                proc.wait()
                stdout.writer.close()
                stderr.writer.close()

                return stdout.reader.read(), stderr.reader.read()


class TestCaseBase(unittest.TestCase):
    CONFIG_YML = os.path.join(os.path.dirname(__file__), "testnodes", "config.yml")
    NODES_CONFIG = r"""nodes:
    pymodule_hello:
        runner: pymodule
        entrypoint: hello
    pymodule_hello2:
        runner: pymodule
        module: testnodes
        entrypoint: hello
    python_hello:
        runner: python
        file: ${comp_dir}/__init__.py
    pymodule_noentrypoint:
        runner: pymodule
    pymodule_invalidmodule:
        runner: pymodule
        module: invalid
        entrypoint: hello
    pymodule_invalidentrypoint:
        runner: pymodule
        entrypoint: invalid
    """

    def write_config(self, value):
        with open(TestCaseBase.CONFIG_YML, "w+") as f:
            f.write(value)

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.write_config(TestCaseBase.NODES_CONFIG)

    def call(
        self,
        argv: Optional[list[str]] = None,
        *,
        has_stdout: bool = None,
        has_stderr: bool = None
    ) -> tuple[str, str]:
        # Run gada node
        stdout, stderr = _run(argv)

        # Check outputs
        if has_stderr is False:
            self.assertEqual(stderr, "", "should have no stderr")
        elif has_stderr is True:
            self.assertNotEqual(stderr, "", "should have stderr")
        if has_stdout is False:
            self.assertEqual(stdout, "", "should have no stdout")
        elif has_stdout is True:
            self.assertNotEqual(stdout, "", "should have stdout")

        # Return outputs
        return stdout.strip(), stderr.strip()
