import click

from grid.client import Grid


@click.group()
def delete() -> None:
    pass


def doublecheck(item: str):
    warning_str = click.style('WARNING!', fg='red')
    message = f"""

    {warning_str}

    Your are about to delete the {item}.
    This will delete all the associated artifacts, logs, and metadata.

    Are you sure you want to do this?

   """
    click.confirm(message, abort=True)


@delete.command()
@click.argument('experiment_ids', type=str, required=True, nargs=-1)
def experiment(experiment_ids: [str]):
    doublecheck(experiment_ids)
    client = Grid()
    for experiment in experiment_ids:
        client.delete(experiment_name=experiment)


@delete.command()
@click.argument('run_ids', type=str, required=True, nargs=-1)
def run(run_ids: [str]):
    doublecheck(run_ids)
    client = Grid()
    for run in run_ids:
        client.delete(run_name=run)
