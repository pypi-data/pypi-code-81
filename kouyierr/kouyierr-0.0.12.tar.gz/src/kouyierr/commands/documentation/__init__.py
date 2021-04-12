from kouyierr.index import index
from kouyierr.commands.documentation.generate import generate


@index.group()
def documentation() -> None:
    pass


def register() -> None:
    documentation.add_command(generate)
