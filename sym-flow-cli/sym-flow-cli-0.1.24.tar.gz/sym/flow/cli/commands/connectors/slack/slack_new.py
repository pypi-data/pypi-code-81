import webbrowser

import click

from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.sym_api_client import SymAPIClient


@click.command(name="new", short_help="Add the Sym App to Slack")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def slack_new(options: GlobalOptions) -> None:
    """Generate a magic link to install the Sym Slack App. This link
    can be opened directly or sent to an administrator with permission to
    install the app into your workspace.
    """

    url = get_magic_url(api_url=options.api_url)
    click.echo("Generated an installation link for the Sym Slack App:\n")
    click.secho(url, fg="white", bold=True)
    click.echo(
        "\nPlease send this URL to an administrator who has permission to install the app.\nOr, if that's you, we can open it now."
    )
    if click.confirm(
        "\nWould you like to open the Slack installation URL in a browser window?",
        default=True,
    ):
        webbrowser.open(url)


def get_magic_url(api_url: str):
    api_client = SymAPIClient(url=api_url)
    url, _ = api_client.get_slack_install_url()
    return url
