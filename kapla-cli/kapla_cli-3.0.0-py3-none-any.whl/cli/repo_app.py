import sys
from pathlib import Path

import typer

from kapla.cli.errors import PyprojectNotFoundError
from kapla.cli.projects import Monorepo
from kapla.cli.utils import run


def create_repo() -> Monorepo:
    yesno = typer.confirm("Do you want to create a new project ?")
    if not yesno:
        raise sys.exit(1)
    run("poetry init")
    repo = Monorepo(Path.cwd())
    repo.set_include_packages([])

    return repo


try:
    repo = Monorepo(Path.cwd())
except PyprojectNotFoundError:
    repo = create_repo()


generator = typer.Typer(
    name="new",
    add_completion=False,
    no_args_is_help=True,
    invoke_without_command=False,
    help="Create new libraries, plugins or applications.",
)


@generator.command("library")
def new_library(name: str) -> None:
    """Create a new library."""
    repo.new_library(name)


@generator.command("plugin")
def new_plugin(name: str) -> None:
    """Create a new plugin."""
    repo.new_plugin(name)


@generator.command("app")
def new_app(name: str) -> None:
    """Create a new application."""
    repo.new_app(name)
