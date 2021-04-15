import csv
import json

import click
import xattr

from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.sym_api_client import SymAPIClient
from sym.flow.cli.helpers.sym_api_service import SymAPIService


def get_users(options: GlobalOptions):
    api_service = SymAPIService(api_client=SymAPIClient(url=options.api_url))
    return api_service.get_user_table_data()


def get_integrations(options: GlobalOptions):
    api_service = SymAPIService(api_client=SymAPIClient(url=options.api_url))
    integration_rows = api_service.get_user_integration_table_data()
    return [
        {
            "type": row[1],
            "name": row[0],
        }
        for row in integration_rows
    ]


@click.command(name="edit", short_help="Edit your Users in a CSV")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.argument("csv_path", type=click.Path(writable=True))
def users_edit(options: GlobalOptions, csv_path: str) -> None:
    users = get_users(options)
    integrations = get_integrations(options)
    fields = ["email"] + [x["name"] for x in integrations]

    with open(csv_path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for user in users:
            writer.writerow(
                dict(
                    {
                        i["integration"]["name"]: i["identifier"]
                        for i in user["identities"]
                    },
                    **{"email": user["email"]},
                )
            )

    connectors = json.dumps({i["name"]: i["type"] for i in integrations}).encode("utf-8")
    xattr.xattr(csv_path).update({"user.sym.connectors": connectors})
