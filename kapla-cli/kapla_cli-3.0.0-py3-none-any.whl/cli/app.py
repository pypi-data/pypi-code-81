from typing import List, Optional

import typer

from kapla.cli.utils import current_directory, run
from kapla.docker.buildx import app as buildx_app

from .release_app import app as release_app
from .repo_app import generator, repo

cli = typer.Typer(
    name="k",
    add_completion=False,
    no_args_is_help=True,
    invoke_without_command=False,
    help="Python monorepo toolkit",
)

cli.add_typer(release_app)
cli.add_typer(generator)
cli.add_typer(buildx_app)


@cli.command("build")
def build(
    format: Optional[str] = None,
    package: Optional[List[str]] = typer.Argument(default=None),
) -> None:
    """Build all packages using poetry."""
    packages = list(package or [])
    repo.build_packages(packages, format)


@cli.command("test")
def test(
    package: Optional[List[str]] = typer.Argument(default=None),
    markers: List[str] = typer.Option(
        [], "--markers", "-m", help="specify markers to run only a subset of tests."
    ),
    exprs: List[str] = typer.Option(
        [],
        "--exprs",
        "-k",
        help="Pytest expression to select tests based on their name.",
    ),
) -> None:
    """Run unit tests using pytest."""
    packages = list(package or [])
    repo.test_packages(packages, markers=markers, exprs=exprs)


@cli.command("bump")
def bump(
    version: str = typer.Argument(
        ..., metavar="VERSION", help="New version to bump to."
    )
) -> None:
    """Bump packages to a new version."""
    repo.bump_packages(version)


@cli.command("lint")
def lint(
    package: Optional[List[str]] = typer.Argument(default=None),
) -> None:
    """Lint all source code using flake8."""
    packages = list(package or [])
    repo.lint_packages(packages)


@cli.command("typecheck")
def typecheck(
    package: Optional[List[str]] = typer.Argument(default=None),
) -> None:
    """Run mypy typechecking againt all source code."""
    packages = list(package or [])
    repo.typecheck_packages(packages)


@cli.command("format")
def format(
    package: Optional[List[str]] = typer.Argument(default=None),
) -> None:
    """Format all source code using black."""
    packages = list(package or [])
    repo.format_packages(packages)


@cli.command("install")
def install(
    package: Optional[List[str]] = typer.Argument(default=None),
) -> None:
    """Install all packages in editable mode and development dependencies."""
    packages = list(package or [])
    repo.install_packages(packages)


@cli.command("clean")
def clean(
    package: Optional[List[str]] = typer.Argument(default=None), dist: bool = True
) -> None:
    """Clean directories."""
    packages = list(package or [])
    repo.clean_packages(packages, no_dist=not dist)


@cli.command("update")
def update(package: Optional[List[str]] = typer.Argument(default=None)) -> None:
    """Update all packages dependencies and generate lock file."""
    packages = list(package or [])
    repo.update_packages(packages)


@cli.command("export")
def export(
    package: Optional[List[str]] = typer.Argument(default=None),
) -> None:
    """Export all packages for offline installation."""
    if not package:
        repo.export_packages()
    else:
        for project in repo.get_packages(list(package)):
            project.export()


@cli.command("coverage")
def coverage() -> None:
    """Start HTML server displaying code coverage."""
    with current_directory(repo.root):
        run("python -m http.server --bind 127.0.0.1 --directory coverage-report")


@cli.command("commit")
def commit() -> None:
    """Commit changes to git repository."""
    with current_directory(repo.root):
        run("cz commit")


@cli.command("config")
def config() -> None:
    """Print config to console."""
    print(repo.config)
