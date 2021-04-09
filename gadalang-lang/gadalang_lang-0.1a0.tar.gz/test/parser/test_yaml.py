"""Test yaml node.
"""
import os
import sys
import asyncio
import pytest
from gadalang_lang import test_utils
from gadalang_lang.test_utils import run, tmp_file


DATA_PATH = test_utils.data_yml_path()
DATA = test_utils.load_yaml(DATA_PATH)


def test_input():
    """Test input parameter."""
    output = run("yaml", {"input": DATA_PATH})

    assert output == {"data": DATA}, "wrong output"


def test_data():
    """Test data parameter."""
    output = run("yaml", {"data": DATA})

    assert output == {"data": DATA}, "wrong output"


def test_output(tmp_file):
    """Test output parameter."""
    output = run("yaml", {"data": DATA, "output": tmp_file.name})
    tmp_file.close()

    assert output == {"data": DATA}, "wrong output"

    # Check output file
    data = test_utils.load_yaml(tmp_file.name)
    assert DATA == data, "wrong output"
