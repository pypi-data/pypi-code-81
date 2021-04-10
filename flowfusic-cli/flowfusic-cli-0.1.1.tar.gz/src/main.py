import click
import sys
from distutils.version import LooseVersion

from src.cli.utils import get_cli_version, is_conda_env
from src.cli.auth import login, logout
from src.cli.version import upgrade, version, auto_upgrade
from src.cli.paraview import paraview
from src.client.version import VersionClient
from src.log import configure_logger


@click.group()
@click.option(
    "-h",
    "--host",
    default="https://www.flowfusic.com",
    help="Flowfusic server endpoint",
)
@click.option("-v", "--verbose", count=True, help="Turn on debug logging")
def cli(host, verbose):
    """
    Flowfusic CLI interacts with Flowfusic server and executes your commands.
    """

    configure_logger(verbose)
    check_cli_version()


def check_cli_version():
    """
    Check if the current cli version satisfies the server requirements
    """
    should_exit = False
    server_version = VersionClient().get_cli_version()
    current_version = get_cli_version()

    if LooseVersion(current_version) < LooseVersion(server_version.min_version):
        print(
            "\nYour version of CLI (%s) is no longer compatible with server."
            % current_version
        )
        should_exit = True
    elif LooseVersion(current_version) < LooseVersion(server_version.latest_version):
        print(
            "\nNew version of CLI (%s) is now available."
            % server_version.latest_version
        )
    else:
        return

    # new version is ready
    if should_exit and click.confirm(
        "\nDo you want to upgrade to version %s now?" % server_version.latest_version
    ):
        auto_upgrade()
        sys.exit(0)
    else:
        msg_parts = []
        msg_parts.append("\nTo manually upgrade run:")
        msg_parts.append("    pip install -U flowfusic-cli")
        if is_conda_env():
            msg_parts.append("We are still working on conda support. Stay tuned!")
        #     msg_parts.append("Or if you prefer to use conda:")
        #     msg_parts.append("    conda install -y -c conda-forge -c floydhub floyd-cli")
        print("\n".join(msg_parts))
        print("")

    if should_exit:
        sys.exit(0)


def add_commands(cli):
    cli.add_command(login)
    cli.add_command(logout)
    cli.add_command(upgrade)
    cli.add_command(version)
    cli.add_command(paraview)


add_commands(cli)
