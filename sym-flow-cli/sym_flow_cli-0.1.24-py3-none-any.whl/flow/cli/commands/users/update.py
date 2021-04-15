from typing import Dict, List

import click

from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.sym_api_client import SymAPIClient
from sym.flow.cli.helpers.sym_api_service import SymAPIService


def patch_user_data(api_url: str, csv_data: str) -> List[Dict[str, str]]:
    api_service = SymAPIService(api_client=SymAPIClient(url=api_url))
    return api_service.patch_user_table_data(csv_data)


@click.command(name="update", short_help="Upload a CSV with new User Identities")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.argument(
    "csv_path",
    type=click.Path(exists=True, readable=True, file_okay=True, dir_okay=False),
)
def users_update(options: GlobalOptions, csv_path: str) -> None:
    with open(csv_path) as f:
        result = patch_user_data(options.api_url, f.read())
    click.secho(f"Successfully updated {len(result)} Users!")
