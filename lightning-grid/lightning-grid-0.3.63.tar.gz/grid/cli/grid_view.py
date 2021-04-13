from typing import List

import click

import grid.globals as env


@click.group()
def view():
    pass


@view.command()
@click.argument('experiment_id', type=str, required=True, nargs=1)
@click.argument('page', type=str, nargs=1, required=False)
def experiment(experiment_id: List[str], page: str) -> None:
    """Grid view shows we web UI page for your runs and experiments."""
    # Fetch URL from globals.
    url = env.GRID_URL.replace('/graphql', '#')

    # Figure out which object is requested
    # so we can construct path.
    base_path = 'view'
    qualifier_path = 'experiment'

    # Combine all strings into a single URL.
    if page:
        launch_url = '/'.join([url, base_path, qualifier_path, experiment_id, page])
    else:
        launch_url = '/'.join([url, base_path, qualifier_path, experiment_id])

    # Open browser.
    click.echo()
    click.echo(f'Opening URL: {launch_url}')
    click.echo()

    click.launch(launch_url)


@view.command()
@click.argument('run_name', type=str, nargs=1)
@click.argument('page', type=str, nargs=1, required=False)
def run(run_name: str, page: str) -> None:
    """Grid view shows we web UI page for your runs and experiments."""
    # Fetch URL from globals.
    url = env.GRID_URL.replace('/graphql', '#')

    # Figure out which object is requested
    # so we can construct path.
    base_path = 'view'
    qualifier_path = 'run'

    # Combine all strings into a single URL.
    if page:
        launch_url = '/'.join([url, base_path, qualifier_path, run_name, page])
    else:
        launch_url = '/'.join([url, base_path, qualifier_path, run_name])

    # Open browser.
    click.echo()
    click.echo(f'Opening URL: {launch_url}')
    click.echo()

    click.launch(launch_url)
