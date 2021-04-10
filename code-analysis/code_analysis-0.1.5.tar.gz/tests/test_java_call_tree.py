#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `code_analysis` package."""
from click.testing import CliRunner

from code_analysis import java_call_tree as jct


def test_java_call_tree():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(jct.main, ['resources/java_call_tree_input.txt'])
    assert result.exit_code == 0
    assert '' in result.output
    assert 'MERGE (n:Class' in result.output
    assert 'MERGE (m:Class' in result.output
    assert 'MERGE (m:Method' in result.output
    assert 'MERGE (n:Method' in result.output
    assert 'MERGE (n)-[r:uses]->(m)' in result.output
    assert 'MERGE (n)-[r:calls]->(m)' in result.output
    assert 'com.company.abc.unit.soundlift.SoundBasedLiftUnitPlugIn' in result.output
    assert 'com.company.abc.unit.soundlift.SoundBasedLiftUnitModel$Property$1:getValue' in result.output


def test_help():
    runner = CliRunner()
    help_result = runner.invoke(jct.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
