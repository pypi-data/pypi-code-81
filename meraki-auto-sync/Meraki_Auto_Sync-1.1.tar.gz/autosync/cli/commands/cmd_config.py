import os

import click
from pathlib import Path
from dotenv import load_dotenv,dotenv_values

@click.group()
def cli():
    """ Tasks to start sync auto Sycn of Meraki Networks """
    pass

@click.command(help='Sets the Meraki API Key as an environment variable')
@click.option('-key','--key', required=True)
def setkey(key):
    os.environ['MERAKI_DASHBOARD_API_KEY'] = key


@click.command(help='Display the Meraki API Key as an environment variable ')
def showkey():
    print(os.getenv('MERAKI_DASHBOARD_API_KEY','No key set please run autosync setkey --key <API Key> to set your key'))


cli.add_command(setkey)
cli.add_command(showkey)
