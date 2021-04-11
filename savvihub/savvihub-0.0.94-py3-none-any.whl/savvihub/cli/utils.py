import inquirer
import typer
from savvihub.api.exceptions import InvalidParametersAPIException, DuplicateAPIException

from openapi_client import ResponseWorkspace
from savvihub import SavviHubClient


def get_default_workspace(client: SavviHubClient) -> ResponseWorkspace:
    workspaces = client.workspace_list().workspaces
    if len(workspaces) == 0:
        region_list_resp = client.region_list()
        typer.echo('Create workspace')
        while True:
            workspace_name = inquirer.prompt([inquirer.Text(
                'workspace_name',
                message="Workspace name",
            )]).get('workspace_name')
            region = inquirer.prompt([inquirer.List(
                'region',
                message="Select region",
                default=region_list_resp.default_region,
                choices=[(region.name, region.value) for region in region_list_resp.regions]
            )]).get('region')
            try:
                default_workspace = client.workspace_create(workspace_name=workspace_name, region=region)
                break
            except InvalidParametersAPIException:
                typer.echo('Invalid workspace name. Please try again.')
            except DuplicateAPIException:
                typer.echo('Duplicate workspace name exist. Please try again.')
    elif len(workspaces) == 1:
        default_workspace = workspaces[0]
        typer.echo(f'Default workspace is automatically set to `{default_workspace.name}`.')
    else:
        default_workspace = inquirer.prompt([inquirer.List(
            'default_workspace',
            message='Select default workspace',
            choices=[(ws.name, ws) for ws in workspaces],
        )]).get('default_workspace')

        typer.echo(f'Default workspace is set to `{default_workspace.name}`.')

    return default_workspace


def find_from_inquirer(options, display, message):
    return inquirer.prompt([inquirer.List(
        "question",
        message=message,
        choices=[(f'[{i+1}] {display(option)}', option) for i, option in enumerate(options)],
    )]).get("question")


def parse_dataset(dataset_full_name):
    if '@' in dataset_full_name:
        dataset_name, snapshot_name = dataset_full_name.split('@', 1)
    else:
        dataset_name = dataset_full_name
        snapshot_name = 'latest'

    if '/' in dataset_name:
        workspace_name, dataset_name = dataset_name.split('/', 1)
    else:
        workspace_name = None

    return workspace_name, dataset_name, snapshot_name
