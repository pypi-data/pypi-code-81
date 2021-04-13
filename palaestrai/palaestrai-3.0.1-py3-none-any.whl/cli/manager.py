#!usr/bin/env python3
# manager.py -- Manager CLI for ARL execution with palaestrAI
# Copyright (C) 2020  OFFIS, All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library.

import logging
import logging.config
import sys

import click
import palaestrai.core.runtime_config
import pkg_resources
from palaestrai.cli import client_local
from palaestrai.core import RuntimeConfig


@click.group()
@click.option(
    "-c",
    "--config",
    type=click.Path(),
    help="Supply custom runtime configuration file. "
    "(Default search path: %s)"
    % (palaestrai.core.runtime_config._RuntimeConfig.CONFIG_FILE_PATHS),
)
@click.option(
    "--verbose",
    "-v",
    count=True,
    help="Increases the program verbosity, can be given numerous times: "
    "-v prints also INFO messages, and -vv emits DEBUG output."
    "output",
)
@click.version_option(pkg_resources.require("palaestrai")[0].version)
def cli(config=None, verbose=0):
    if config:
        try:
            with open(config, "r") as fp:
                RuntimeConfig().load(fp)
        except OSError as e:
            click.echo(
                "ERROR: Could not load config from %s: %s." % (config, e),
                file=sys.stderr,
            )
            exit(1)
    else:
        try:
            RuntimeConfig().load()
        except FileNotFoundError as e:
            click.echo(
                "Please create a runtime config (one of %s), "
                % (config.CONFIG_FILE_PATHS),
                file=sys.stderr,
            )
            click.echo("%s." % e, file=sys.stderr)
            exit(1)
    init_logger(verbose)


def init_logger(verbose):
    """Init logger with config from either RuntimeConfig or a default."""
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    log_level = levels[verbose if verbose < len(levels) else len(levels) - 1]

    try:
        logging.config.dictConfig(RuntimeConfig().logging)
        logging.debug(
            "Initialized logging from RuntimeConfig(%s)", RuntimeConfig()
        )
    except (KeyError, ValueError) as e:
        logging.basicConfig(level=log_level)
        logging.warning(
            "Could not load logging config (%s), " "continuing with defaults",
            e,
        )
    if verbose != 0:
        for name in logging.root.manager.loggerDict:
            logging.getLogger(name).setLevel(log_level)


for cmd in [
    client_local.experiment_start,
    client_local.database_create,
    client_local.database_migrate,
]:
    cli.add_command(cmd)


if __name__ == "__main__":
    cli()
