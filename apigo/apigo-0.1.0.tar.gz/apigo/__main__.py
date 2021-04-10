# type: ignore[attr-defined]

from typing import Optional

import random
from enum import Enum

import typer
from apigo import __version__
from apigo.example import hello


class Color(str, Enum):
    white = "white"
    red = "red"
    cyan = "cyan"
    magenta = "magenta"
    yellow = "yellow"
    green = "green"


app = typer.Typer(
    name="apigo",
    help="get a fast REST mock server out of the box",
    add_completion=False,
)


def version_callback(value: bool):
    """Prints the version of the package."""
    if value:
        typer.echo(f"[yellow]apigo[/] version: [bold blue]{__version__}[/]")
        raise typer.Exit()


@app.command(name="")
def main(
    name: str = typer.Option(..., help="Name of person to greet."),
    version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the apigo package.",
    ),
):
    """Prints a greeting for a giving name."""
    greeting: str = hello(name)
    typer.echo(f"{greeting}")
