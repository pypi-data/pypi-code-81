#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `code_analysis` package."""
from click.testing import CliRunner

from code_analysis import python_dependencies as pyd


def test_python_dependencies():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(pyd.main, ['code_analysis'])
    assert result.exit_code == 0
    assert 'code_analysis.python_dependencies' in result.output
    assert 'MERGE (n:Package' in result.output
    assert 'MERGE (m:Module' in result.output
    assert 'MERGE (n)-[r:contains]->(m)' in result.output
    assert 'MERGE (n)-[r:uses]->(m)' in result.output


def test_help():
    runner = CliRunner()
    help_result = runner.invoke(pyd.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
