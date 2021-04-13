#!/usr/bin/env python3

import click

__author__ = "Catalin Dinuta"

from .cli_constants import CLIConstants
from .env_constants import EnvConstants
from .environment import EnvironmentSingleton
from .generator import Generator


@click.command()
@click.option('--infile', help="The input file to be used for report generator. E.g. results.json")
@click.option('--outfile',
              help="The desired output file name. The default value is 'results.xls'. E.g. Regression_20.xlsx")
def cli(infile, outfile):
    env = EnvironmentSingleton.get_instance()
    infile = infile if infile is not None else env.get_env_and_virtual_env().get(EnvConstants.IN_FILE)
    outfile = outfile if outfile is not None else env.get_env_and_virtual_env().get(EnvConstants.OUT_FILE)
    generator = Generator(json_file=infile, excel_file=outfile)

    try:
        generator.generate()
    except Exception as e:
        click.echo(e.__str__())
        exit(CLIConstants.FAILURE)

    exit(CLIConstants.SUCCESS)


if __name__ == "__main__":
    cli()
