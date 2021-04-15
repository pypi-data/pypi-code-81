import click
from sym.cli.helpers.sym_group import SymGroup

from sym.flow.cli.helpers.global_options import GlobalOptions

from .slack_delete import slack_delete
from .slack_list import slack_list
from .slack_new import slack_new


@click.group(cls=SymGroup, short_help="Perform operations on Sym Slack Connectors")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def slack(options: GlobalOptions) -> None:
    """Sym Flow CLI commands for operations on Slack Connectors."""


slack.add_command(slack_new)
slack.add_command(slack_delete)
slack.add_command(slack_list)
