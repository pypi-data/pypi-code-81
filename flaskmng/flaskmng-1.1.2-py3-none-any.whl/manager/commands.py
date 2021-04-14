import click
from ..utils import MultiCommand

@click.group(cls=MultiCommand)
def manager():
    pass

@manager.command("startproject")
def startproject_command():
    print("STARTING PROJECT")

@manager.command("newapp")
def startproject_command():
    print("NEW APP")