# -*- coding: utf-8 -*-
"""Some utility tools used in tests.
"""
from __future__ import annotations

__all__ = ["testnodes_path", "write_testnodes_config"]
import os
import yaml
from typing import Optional
import gada


def testnodes_path() -> str:
    """Get the absolute path to ``gada_pyrunner/test/testnodes``.

    :return: path to testnodes directory
    """
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "test", "testnodes")
    )


def write_testnodes_config(config: dict):
    """Overwrite ``gada_pyrunner/test/testnodes/config.yml``.

    :param config: new configuration
    """
    with open(os.path.join(testnodes_path(), "config.yml"), "w+") as f:
        f.write(yaml.safe_dump(config))
