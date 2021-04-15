import click
from sym.cli.helpers.sym_group import SymGroup

from sym.flow.cli.helpers.global_options import GlobalOptions

from .slack import slack_commands


@click.group(cls=SymGroup, short_help="Perform operations on Sym Connectors")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def connectors(options: GlobalOptions) -> None:
    """Sym Flow CLI commands for operations on Connectors."""


connectors.add_command(slack_commands)
