import sys
import click

from .utils import process_ok, MultiCommand

@click.group(cls=MultiCommand)
def main():
    pass

from .startproject import startproject_command
from .startapp import startapp_command
from .removeapp import removeapp_command


def command_line_interface():
    args = sys.argv
    if "--help" in args or len(args) == 1:
        process_ok([], False)
    try:
        main()
    except Exception as e:
        print("❌ "+str(e))
