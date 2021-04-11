import logging

import typer

from smoothtransitions.subcommands import (
    gaussian_io,
    reporting,
    runner,
    workflow,
    workflow_log,
)

logger = logging.getLogger(__name__)

app = typer.Typer()
app.command()(gaussian_io.io)
app.command()(reporting.report)
app.command()(runner.runner)
app.command()(workflow.workflow)
app.command()(workflow_log.workflow_log)

if __name__ == "__main__":
    app()
