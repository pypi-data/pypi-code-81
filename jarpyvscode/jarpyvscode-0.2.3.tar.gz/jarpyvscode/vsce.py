"""Command line interface wrapping calls of the tool ``vsce``."""

# Standard library:
import platform
import shlex
import subprocess
import sys
from pathlib import Path

# 3rd party:
import click

# local:
from jarpyvscode.log import get_log_level_from_cli, logger, logwrap


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option(
    "--debug/--no-debug",
    default=False,
    show_default=True,
    help="Print debug level log messages",
)
@click.pass_context
@logwrap()
def cli(ctx: click.Context, verbose: int = 0, debug: bool = False) -> None:
    """Command line interface wrapping calls of the tool ``vsce``."""
    logger.remove()
    level: str = get_log_level_from_cli(debug=debug, verbose=verbose)
    logger.add(sys.stderr, level=level)
    logger.info(
        f"CLI: Invoked sub command: '{ctx.invoked_subcommand}' "
        f"with log level '{level}'."
    )


@cli.command()  # type: ignore
@logwrap()
def pack():
    """Pack VSCode extension."""
    vsix_file: Path
    for vsix_file in Path.glob(self=Path.cwd(), pattern="*.vsix"):
        if vsix_file.is_file():
            logger.info(f"Remove '{vsix_file}' ...")
            vsix_file.unlink()
    cmd: str = "vsce.cmd" if "windows" in platform.platform().lower() else "vsce"
    cmd += " package -o dist/"
    try:
        logger.info(f"Execute '{cmd}' ...")
        sys.exit(subprocess.check_call(shlex.split(cmd)))
    except subprocess.CalledProcessError as e:
        logger.error(f"Packing extension failed: {e}")
        sys.exit(e.returncode)


@cli.command()  # type: ignore
@logwrap()
def publish():
    """Publish VSCode extension."""
    cmd: str = "vsce.cmd" if "windows" in platform.platform().lower() else "vsce"
    cmd += " publish"
    try:
        logger.info(f"Execute '{cmd}' ...")
        sys.exit(subprocess.check_call(shlex.split(cmd)))
    except subprocess.CalledProcessError as e:
        logger.error(f"Publishing extension failed: {e}")
        sys.exit(e.returncode)


@cli.command()  # type: ignore
@logwrap()
def unpublish():
    """Unpublish VSCode extension."""
    cmd: str = "vsce.cmd" if "windows" in platform.platform().lower() else "vsce"
    cmd += " unpublish --force"
    try:
        logger.info(f"Execute '{cmd}' ...")
        sys.exit(subprocess.check_call(shlex.split(cmd)))
    except subprocess.CalledProcessError as e:
        logger.error(f"Unpublishing extension failed: {e}")
        sys.exit(e.returncode)


if __name__ == "__main__":
    cli(obj={})
    sys.exit(0)
