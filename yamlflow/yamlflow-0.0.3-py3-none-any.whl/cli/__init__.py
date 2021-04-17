import click

from yamlflow.cli._version import version
from yamlflow.cli._build import build


@click.group()
def main():
    """ML model server that works"""
    pass


main.add_command(version)
main.add_command(build)
