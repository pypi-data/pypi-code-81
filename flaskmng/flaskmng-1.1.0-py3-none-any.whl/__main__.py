import sys
import click

from .startproject import startproject
from .startapp import startapp
from .removeapp import removeapp
from .utils import process_ok

commands = [
    startproject,
    startapp,
    removeapp
]


main = click.CommandCollection(sources=commands)

def command_line_interface():
    args = sys.argv
    if "--help" in args or len(args) == 1:
        process_ok([],False)
    try:
        main()
    except Exception as e:
        print("❌ "+str(e))
