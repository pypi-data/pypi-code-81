"""Test json node.
"""
import os
import sys
import asyncio
import pytest
from gadalang_lang import test_utils
from gadalang_lang.test_utils import run, tmp_file


DATA_PATH = test_utils.data_json_path()
DATA = test_utils.load_json(DATA_PATH)


def test_input():
    """Test input parameter."""
    output = run("json", {"input": DATA_PATH})

    assert output == {"data": DATA}, "wrong output"


def test_data():
    """Test data parameter."""
    output = run("json", {"data": DATA})

    assert output == {"data": DATA}, "wrong output"


def test_output(tmp_file):
    """Test output parameter."""
    output = run("json", {"data": DATA, "output": tmp_file.name})
    tmp_file.close()

    assert output == {"data": DATA}, "wrong output"

    # Check output file
    data = test_utils.load_json(tmp_file.name)
    assert DATA == data, "wrong output"
