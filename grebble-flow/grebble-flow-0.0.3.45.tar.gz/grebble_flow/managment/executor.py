import click
import grpc

from grebble_flow.grpc import manager


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--port", help="Port", type=int, default=5000,
)
@click.option(
    "--debug",
    help="Debug",
    type=bool,
    default=False,
    required=False,
    show_default=True,
)
@click.option(
    "--socket",
    help="Socket",
    type=str,
    default=False,
    required=False,
    show_default=True,
)
def runprocessor(port=5000, debug=False, socket=False):
    manager.start_server(port)
