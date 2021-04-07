import sys
import click

from .startproject import startproject
from .startapp import startapp

commands = [
    startproject,
    startapp
]


main = click.CommandCollection(sources=commands)

if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("flaskmng")
    try:
        main()
    except Exception as e:
        print("❌ "+str(e))
