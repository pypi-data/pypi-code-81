# -*- coding: utf-8 -*-
"""Some utility tools used in tests.
"""
from __future__ import annotations

__all__ = [
    "data_path",
    "data_json_path",
    "data_yml_path",
    "run",
    "load_json",
    "load_yaml",
    "tmp_file",
]
import os
import unittest
import pytest
import asyncio
import json
import yaml
import tempfile
import pygada_runtime


def data_path() -> str:
    """Get the absolute path to ``test/data``.

    :return: path to data directory
    """
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "test", "data")
    )


def data_json_path() -> str:
    """Get the absolute path to ``test/data/data.json``.

    :return: path to data.json file
    """
    return os.path.join(data_path(), "data.json")


def data_yml_path() -> str:
    """Get the absolute path to ``test/data/data.yml``.

    :return: path to data.yml file
    """
    return os.path.join(data_path(), "data.yml")


def run(node: str, params: dict = None):
    async def _run():
        with pygada_runtime.PipeStream() as stdin:
            with pygada_runtime.PipeStream() as stdout:
                with pygada_runtime.PipeStream(rmode="r") as stderr:
                    pygada_runtime.write_json(stdin, params)
                    stdin.eof()

                    proc = await pygada_runtime.run(
                        f"gadalang_lang.{node}",
                        stdin=stdin.reader,
                        stdout=stdout,
                        stderr=stderr,
                    )

                    await proc.wait()

                    stdout.eof()
                    stderr.eof()

                    if proc.returncode != 0:
                        raise Exception(await stderr.read())

                    return await pygada_runtime.read_json(stdout)

    return asyncio.run(_run())


def load_json(filename: str) -> dict:
    """Load a JSON file;

    .. code-block:: python

        >>> from gadalang_lang import test_utils
        >>>
        >>> test_utils.load_json(test_utils.data_json_path())
        {'a': 1, 'b': 2}
        >>>

    :param filename: file to load
    :return: JSON object
    """
    with open(filename, "r") as f:
        return json.loads(f.read())


def load_yaml(filename: str) -> dict:
    """Load a YAML file;

    .. code-block:: python

        >>> from gadalang_lang import test_utils
        >>>
        >>> test_utils.load_yaml(test_utils.data_yml_path())
        {'a': 1, 'b': 2}
        >>>

    :param filename: file to load
    :return: JSON object
    """
    with open(filename, "r") as f:
        return yaml.safe_load(f.read())


@pytest.fixture
def tmp_file():
    """Create a temporary file and delete it afterward.

    :return: temporary file
    """
    f = tempfile.NamedTemporaryFile(delete=False)
    yield f
    f.close()
    os.remove(f.name)
