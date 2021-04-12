import click

from kouyierr import __version__


@click.group(context_settings=(dict(max_content_width=120)))
def index() -> None:
    pass


@click.command()
def version() -> None:
    print(__version__)


def register() -> None:
    index.add_command(version)
