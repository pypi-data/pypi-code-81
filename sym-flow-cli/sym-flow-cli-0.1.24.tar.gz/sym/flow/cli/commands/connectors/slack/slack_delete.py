import webbrowser

import click

from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.sym_api_client import SymAPIClient


@click.command(name="delete", short_help="Remove the Sym App from Slack")
@click.option(
    "--workspace-id",
    required=True,
    prompt="Slack Workspace ID",
    help="The ID of the Slack workspace to remove the Sym app from",
)
@click.make_pass_decorator(GlobalOptions, ensure=True)
def slack_delete(options: GlobalOptions, workspace_id: str) -> None:
    """Uninstall the Sym Slack App from a workspace. This will completely
    revoke Sym's access in the workspace, and delete any data associated with
    the connector in Sym's system.

    To see what workspaces the Sym App is installed in, and the corresponding
    Workspace IDs, use `symflow connectors slack list`.
    """

    slack_uninstall(options.api_url, workspace_id)
    click.echo(
        "Uninstall successful! The Sym App has been removed from your Slack workspace."
    )


def slack_uninstall(api_url: str, workspace_id: str):
    api_client = SymAPIClient(url=api_url)
    api_client.uninstall_slack(workspace_id)
