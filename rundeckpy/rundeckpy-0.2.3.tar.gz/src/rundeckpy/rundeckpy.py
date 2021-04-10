"""Rundeckpy CLI."""

import click

@click.command()
@click.argument("plugin")
def install(plugin):
    """Parse a timezone and greet a location a number of times."""
    print(f"Hello, {plugin}!")
