from typing import Dict
try:
    from rich.console import Console
    from rich.table import Table
    from rich.tree import Tree
    from rich.panel import Panel
    from rich import box
except ImportError:
    raise ImportError(
        "You need to install the extra 'cmd', e.g. pip install threedi-settings[cmd]"  # noqa
    )


console = Console()


class OverViewTable:

    def __init__(self, available_ids: Dict):
        self.available_ids = available_ids

    @property
    def table(self):

        t = Table(
            box=box.HORIZONTALS,
            title="v2_global_settings",
            min_width=int((console.width * 30) / 100))
        t.add_column("ID", style="cyan")
        t.add_column("Name", style="green")
        for id, name in self.available_ids.items():
            t.add_row(str(id), name)
        return t
