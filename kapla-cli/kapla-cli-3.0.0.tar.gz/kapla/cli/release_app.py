import os
import pathlib
import shutil
from contextlib import contextmanager
from typing import Iterator

import typer
from loguru import logger

from kapla.cli.utils import run

RC_BRANCH_NAME = os.environ.get("RC_BRANCH_NAME", "next")
STABLE_BRANCH_NAME = os.environ.get("STABLE_BRANCH_NAME", "stable")


@contextmanager
def ensure_config() -> Iterator[pathlib.Path]:
    config = pathlib.Path.cwd() / "release.config.js"
    if not config.exists():
        shutil.copy2(pathlib.Path(__file__).parent / "release.config.js", config)
    try:
        logger.debug(f"Using config: {config.read_text()}")
        yield config
    finally:
        config.unlink(missing_ok=True)


app = typer.Typer(
    name="release",
    add_completion=False,
    no_args_is_help=True,
    invoke_without_command=False,
    help="Python monorepo release toolkit",
)


@app.command("prepare")
def prepare_release(
    version: str = typer.Option(...), branch: str = typer.Option(...)
) -> None:
    """Prepare the release."""
    # Make sure to start from given branch
    run(f"git checkout {branch}")
    # Update version using command defined above
    run(f"k bump {version}")
    # At this point semantic release already performed a commit
    run("git add .")
    # Commit changes to the current branch
    run(f"git commit -m 'chore(release): bumped to version {version}'")


@app.command("publish")
def publish_release(branch: str = typer.Option(...)) -> None:
    """Perform the release."""
    # Checkout target branch
    run(f"git checkout {branch}")
    # Push changes into target branch
    run(f"git push origin {branch}")


@app.command("success")
def on_success(branch: str = typer.Option(...)) -> None:
    """Merge changes back into next on success on stable releases only."""
    if branch == STABLE_BRANCH_NAME:
        # Checkout release candidate branch ("next" by default)
        run(
            f"git switch -c {RC_BRANCH_NAME} 2>/dev/null || git checkout {RC_BRANCH_NAME}"
        )
        # Merge changes from stable branch
        run(
            f"git merge --no-ff origin/{branch} -m 'chore(release): merge from stable branch [skip ci]'"
        )
        # Push changes into release candidate branch ("next" by default)
        run(f"git push origin {RC_BRANCH_NAME}")


@app.command("dry-run")
def dry_run() -> None:
    """Perform a release dry-run."""
    with ensure_config():
        run("semantic-release --dry-run --debug")


@app.command("do")
def do_release() -> None:
    """Perform a release."""
    with ensure_config():
        run("semantic-release --debug")


@app.command("install")
def install_deps(become: bool = False) -> None:
    """Install release dependencies"""
    deps = [
        "semantic-release",
        "@semantic-release/commit-analyzer",
        "@semantic-release/changelog",
        "@semantic-release/exec",
        "conventional-changelog-conventionalcommits",
    ]
    cmd = "npm i -g " + " ".join(deps)
    if become:
        cmd = "sudo " + cmd
    logger.debug(f"Running command: {cmd}")
    run(cmd)
