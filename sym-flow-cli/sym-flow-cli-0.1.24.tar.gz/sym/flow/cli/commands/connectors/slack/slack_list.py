import click
from tabulate import tabulate

from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.sym_api_client import SymAPIClient
from sym.flow.cli.helpers.sym_api_service import SymAPIService


@click.command(name="list", short_help="List Sym Slack App installations")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def slack_list(options: GlobalOptions) -> None:
    """Lists out information about what Slack workspaces the Sym Slack App is
    installed in.
    """

    click.echo(get_slack_connector_data(options.api_url))


def get_slack_connector_data(api_url: str):
    api_service = SymAPIService(api_client=SymAPIClient(url=api_url))
    return tabulate(
        api_service.get_slack_connectors_table_data(),
        headers=["Workspace Name", "Workspace ID"],
    )
