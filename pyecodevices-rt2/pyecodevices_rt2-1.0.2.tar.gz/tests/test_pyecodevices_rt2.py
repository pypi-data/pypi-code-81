#!/usr/bin/env python

"""Tests for `pyecodevices_rt2` package."""
from click.testing import CliRunner

from pyecodevices_rt2 import EcoDevicesRT2
from pyecodevices_rt2 import cli

import os
from dotenv import load_dotenv
import logging

_LOGGER = logging.getLogger(__name__)
load_dotenv()

ECORT2_HOST = os.environ.get("ECORT2_HOST", "")
ECORT2_PORT = os.environ.get("ECORT2_PORT", 80)
ECORT2_APIKEY = os.environ.get("ECORT2_APIKEY", "")


def test_ping():
    """Sample pytest test function with the pytest fixture as an argument."""
    if (ECORT2_APIKEY != ""):
        ecodevices = EcoDevicesRT2(ECORT2_HOST, ECORT2_PORT, ECORT2_APIKEY)
        _LOGGER.debug("# ping")
        assert ecodevices.ping()
    else:
        _LOGGER.warning("""No host/apikey defined in environement variable for GCE Ecodevices RT2.
Test 'ping' not started.""")


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'pyecodevices_rt2.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
