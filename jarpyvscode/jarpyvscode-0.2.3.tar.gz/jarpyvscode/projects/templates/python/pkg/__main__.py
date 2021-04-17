"""Command line interface for ${PROJECT_NAME}."""

# Standard library:
import sys
from pathlib import Path

# 3rd party:
import click

# Extend sys.path:
PROJECT_DIR: Path = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

# local:
import ${PROJECT_NAME}.constants as c
from ${PROJECT_NAME}.log import get_log_level_from_cli, logwrap, logger


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option(
    "--debug/--no-debug",
    default=False,
    envvar="DEBUG",
    show_default=True,
    help="Print debug level log messages",
)
@click.pass_context
@logwrap()
def cli(ctx: click.Context, verbose: int = 0, debug: bool = False) -> None:
    """Command line interface for ${PROJECT_NAME}."""
    logger.remove()
    level: str = get_log_level_from_cli(debug=debug, verbose=verbose)
    log_file_path: Path = c.LOG_DIR / f"{c.PROJECT_NAME}.log"
    logger.add(sys.stderr, level=level)
    logger.add(log_file_path, level="INFO")
    logger.add(str(log_file_path).replace(".log", "_debug.log"), level="DEBUG")
    logger.notice(
        f"CLI: Invoked sub command: '{ctx.invoked_subcommand}' "
        f"with console log level '{level}'."
    )
    ctx.obj["DEBUG"] = debug
    ctx.obj["LOG_LEVEL"] = level


@cli.command(help="")  # type: ignore
@click.argument("name", default=None, required=True, type=str)
@click.pass_context
@logwrap()
def hello(ctx: click.Context, name: str):
    """Say hello to *name*."""
    logger.trace(f"Hello '{name}'!")
    logger.debug(f"Hello '{name}'!")
    logger.info(f"Hello '{name}'!")
    logger.notice(f"Hello '{name}'!")
    logger.warning(f"Hello '{name}'!")
    logger.error(f"Hello '{name}'!")
    logger.critical(f"Hello '{name}'!")


if __name__ == "__main__":
    cli(obj={})
