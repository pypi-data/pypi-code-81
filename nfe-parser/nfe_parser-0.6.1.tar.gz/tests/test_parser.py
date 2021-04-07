#!/usr/bin/env python

"""Tests for `nfe_parser` module."""

import pytest

from nfe_parser.nfe_parser import parse_nfe_from_file


@pytest.fixture(params=range(0, 30))
def file_index(request):
    return request.param


@pytest.fixture()
def file_path(request, file_index):
    return f"tests/nfes/nfe_{file_index:02d}.html"


def test_parse_file(file_path):
    parse_nfe_from_file(file_path)
