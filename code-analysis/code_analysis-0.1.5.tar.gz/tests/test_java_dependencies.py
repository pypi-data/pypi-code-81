#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `code_analysis` package."""
from click.testing import CliRunner

from code_analysis import java_dependencies as jvd


def test_java_dependencies():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(jvd.main, ['resources/java_depend.txt'])
    assert result.exit_code == 0
    assert 'MERGE (n:Package' in result.output
    assert 'MERGE (m:Package' in result.output
    assert 'MERGE (n)-[r:depends_on]->(m)' in result.output
    assert 'com.company.abc.plaza.storage.ifc' in result.output
    assert 'com.company.abc.general.basic.ifc.configuration' in result.output


def test_help():
    runner = CliRunner()
    help_result = runner.invoke(jvd.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
