import click

from grid.client import Grid


@click.command()
def history() -> None:
    """View list of historic Runs."""
    client = Grid()
    client.history()
