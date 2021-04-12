from kouyierr.index import index
from kouyierr.commands.ghproject.generate import generate


@index.group()
def ghproject() -> None:
    pass


def register() -> None:
    ghproject.add_command(generate)
