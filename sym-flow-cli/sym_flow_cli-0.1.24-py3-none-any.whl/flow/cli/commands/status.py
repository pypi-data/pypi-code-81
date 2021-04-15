import sys

import click

from sym.flow.cli.errors import CliErrorWithHint
from sym.flow.cli.helpers.config import Config
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.sym_api_client import SymAPIClient
from sym.flow.cli.helpers.sym_api_service import SymAPIService


def fail(message):
    click.secho(f"✖ {message}!", fg="red", bold=True)
    click.secho(f"Try running `symflow login`.", fg="cyan")
    sys.exit(1)


@click.command(short_help="Check your stored auth token")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def status(options: GlobalOptions) -> None:
    if not Config.is_logged_in():
        fail("No user found")

    org = Config.get_org()["slug"]
    email = Config.get_email()
    api_service = SymAPIService(api_client=SymAPIClient(url=options.api_url))

    if not api_service.verify_login(email):
        fail("Token expired")

    click.secho(f"✔️  Status check succeeded!", fg="green")
    click.echo(
        f"   You are logged in to {click.style(org, bold=True)} as {click.style(email, bold=True)}."
    )
