import logging
import pathlib

import typer
from tabulate import tabulate

from .utils.utils import load_project_file

logger = logging.getLogger(__name__)


def workflow_log(
    log_file: pathlib.Path = typer.Argument(
        "project.log", help="Location of the project log file"
    )
) -> None:
    """Small command to print the workflow log nicely in the terminal."""
    if log_file.exists():
        data = load_project_file(log_file)
        data = data.fillna("")
        data = data.sort_values(["conf", "iteration"])
        header = data.columns.tolist()
        logging.info(
            # added the newline there to not mess with the table format
            "\n"
            + tabulate(data, headers=header, showindex="never", tablefmt="orgtbl")
        )
    else:
        typer.echo(
            (
                f"No log file with the name {log_file} found. "
                "Please specify a log file"
            )
        )
