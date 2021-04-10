from pathlib import Path

import typer

from kapla.cli.projects import Monorepo
from kapla.cli.utils import run


def create_repo() -> Monorepo:
    typer.confirm("Do you want to create a new project ?")
    run("poetry init")
    repo = Monorepo(Path.cwd())
    repo.set_include_packages([])
    return repo
