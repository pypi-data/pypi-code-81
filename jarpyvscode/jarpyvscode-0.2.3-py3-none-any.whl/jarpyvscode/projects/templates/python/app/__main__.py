"""FastAPI app CLI."""

# Standard library:
import sys
from pathlib import Path

# 3rd party:
import click
import uvicorn

# Extend sys.path:
PROJECT_DIR: Path = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

# local:
import ${PROJECT_NAME}.constants as c
from ${PROJECT_NAME}.log import get_log_level_from_cli, logwrap, logger

logger.remove()
logger.add(sys.stderr, format="{time} {level} {message}", level="DEBUG")


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


@cli.command(help="Start FastAPI app server")
@click.option("--host", default="0.0.0.0", required=False, type=str, show_default=True)
@click.option("--port", default=8000, required=False, type=int, show_default=True)
@click.option(
    "--reload/--no-reload", default=False, required=False, type=bool, show_default=True
)
@click.option(
    "--reload-delay",
    default=1.0,
    required=False,
    type=float,
    show_default=True,
    help="Delay [s] between previous and next check",
)
@click.option(
    "--root-path",
    default="/",
    required=False,
    type=str,
    show_default=True,
    help=(
        "Set the ASGI 'root_path' for applications "
        "submounted below a given URL path/ behind a proxy. "
        "Example value: '/project_name'"
    ),
)
@click.pass_context
@logwrap()
def start(
    ctx: click.Context,
    host: str,
    port: int,
    reload: bool,
    reload_delay: float,
    root_path: str,
):
    """Start FastAPI app server."""
    logger.info(f"Start uvicorn to listen on '{host}:{port}' ...")
    uvicorn.run(
        app="application:app",
        host=host,
        port=port,
        reload=reload,
        reload_delay=reload_delay,
        root_path=root_path,
        log_level=ctx.obj["LOG_LEVEL"].lower(),
    )


if __name__ == "__main__":
    cli(obj={})
