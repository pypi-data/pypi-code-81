from typing import Optional

import click

from grid.client import Grid
import grid.globals as env
from grid.types import ObservableType
from grid.utilities import is_experiment


def _check_is_experiment(ctx, _param, value):
    """Callback that checks if a value is an experiment."""
    if not value:
        return value

    if is_experiment(value):
        raise click.BadArgumentUsage(f"Must pass a Run name, not Experiment: {value}")

    return value


@click.command()
@click.argument('run', type=str, nargs=1, required=False, callback=_check_is_experiment)
@click.option('--follow', type=bool, help='Follows Run setup progress in terminal', is_flag=True)
@click.option('--details', type=bool, help='Shows Run submission details', is_flag=True)
@click.option('--export',
              type=click.Choice(['csv', 'json'], case_sensitive=False),
              help='Exports status output to supplied file type')
def status(run: Optional[str] = None,
           follow: Optional[bool] = False,
           details: Optional[bool] = False,
           export: Optional[str] = None) -> None:
    """Checks the status of Runs and Experiments."""
    client = Grid()

    # Setup global flag to show build errors with
    # Runs or Experiments. This is more effective than
    # passing the flag around through all the invocations.
    env.SHOW_PROCESS_STATUS_DETAILS = details

    # Users can see the statuses of Experiments
    # by selecting runs.
    kind = ObservableType.RUN
    observable = []
    if run:
        observable = [run]
        kind = ObservableType.EXPERIMENT

    client.status(kind=kind, identifiers=observable, follow=follow, export=export)

    # If we have a Run, then don't print the global
    # interactive nodes table.
    if not run:
        client.status(kind=ObservableType.INTERACTIVE, identifiers=observable, follow=follow, export=export)
