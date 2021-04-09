import os
import warnings

import click
import pytest
from flask.cli import with_appcontext
from flask.globals import current_app

from .generator import g_init_test, g_unit_test


@click.group("test")
def group():
    """
    Unit testing tools.
    """


@group.command()
@with_appcontext
def init():
    """
    Initialization projects with unit testing.
    """

    g_init_test()


@group.command()
@click.argument("name")
@with_appcontext
def new(name):
    """
    Create a new unit test.
    """

    g_unit_test(name)


@group.command(context_settings=dict(ignore_unknown_options=True))
@with_appcontext
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def run(args):
    """
    Run unit tests.
    """

    warnings.filterwarnings("ignore", "Module already imported")
    os.chdir(current_app.root_path)
    pytest.main(list(args))
