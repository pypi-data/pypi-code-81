from pathlib import Path

from threedi_settings.threedimodel_config import ThreedimodelSqlite
from threedi_settings.pretty.output.global_settings import OverViewTable
try:
    import typer
    from rich.console import Console
    from rich.tree import Tree
    from rich.panel import Panel
except ImportError:
    raise ImportError(
        "You need to install the extra 'cmd', e.g. pip install threedi-settings[cmd]"  # noqa
    )

global_settings_app = typer.Typer()

console = Console()


@global_settings_app.command()
def ls(
    sqlite_file: Path = typer.Argument(
        ...,
        exists=True,
        dir_okay=False,
        writable=False,
        resolve_path=True,
        help="SQLITE model file.",
    ),
):
    """Shows id and name of existing global settings entries"""
    tms = ThreedimodelSqlite(sqlite_file, ...)
    ht = OverViewTable(tms.get_global_settings_ids())
    console.print(
        f"[green] The sqlite file contains the following global settings rows:"
    )
    console.print(ht.table)


@global_settings_app.callback()
def main():
    pass


if __name__ == "__main__":
    global_settings_app()
