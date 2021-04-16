import click
from pathlib import Path
from dotenv import load_dotenv,dotenv_values

@click.group()
def cli():
    """ Tasks to start sync auto Sycn of Meraki Networks """
    pass

@click.command(help='Load environment variable file')
@click.option('-f','--file', default='~/.env',
              show_default='~/.env')
def loadenv(file):
    dotenv_path = Path(file)
    load_dotenv(dotenv_path=dotenv_path,verbose=True)


@click.command(help='Display environment variable file content')
@click.option('-f','--file', default='~/.env',
              show_default='~/.env')
def readenv(file):
    dotenv_path = Path(file)
    dotenv_values(dotenv_path=dotenv_path,verbose=True)


cli.add_command(loadenv)
cli.add_command(readenv)
