from kouyierr.index import index
from kouyierr.commands.invoice.generate import generate


@index.group()
def invoice() -> None:
    pass


def register() -> None:
    invoice.add_command(generate)
