import click

import src
from src.log import configure_logger
from src.main import add_commands, check_cli_version


@click.group()
@click.option("-v", "--verbose", count=True, help="Turn on debug logging")
def cli(verbose):
    """
    Flowfusic CLI interacts with Flowfusic server and executes your commands.
    More help is available under each command listed below.
    """

    src.CLOUD_HTTPS_ENDPOINT = "https://api.gcp.flowfusic.com:5000"
    src.CLOUD_SOCKET_ENDPOINT = ("api.gcp.flowfusic.com", 5001)

    configure_logger(verbose)
    check_cli_version()


add_commands(cli)
