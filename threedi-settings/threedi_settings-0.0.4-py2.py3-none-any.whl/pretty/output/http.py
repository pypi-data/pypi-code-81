from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

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

from openapi_client.models.simulation_settings_overview import SimulationSettingsOverview

console = Console()


class TreeMixin:
    """tree instance is shared between subclasses"""

    # tree template
    tree = Tree("")


class SetttingsTreeBase(TreeMixin):
    SKIP_FIELDS = {"id", "simulation_id", "url"}

    def __init__(self, name: str, data):
        self.name = name
        self.data = data

    def add_branch(self):
        _data = self.data.to_dict()
        sub_tree = self.tree.add(f"[green]{self.name} [ID {_data['id']}]")
        for field, value in _data.items():
            if field in self.SKIP_FIELDS:
                continue
            sub_tree.add(f"[blue]{field}: [bold cyan]{value}")

    def show(self):
        console.print(self.tree)


class GeneralSettingsTree(SetttingsTreeBase):

    def __init__(self, data):
        super().__init__(f"general settings", data)


class TimeStepSettingsTree(SetttingsTreeBase):

    def __init__(self, data):
        super().__init__(f"time step settings", data)


class NumericalSettingsTree(SetttingsTreeBase):

    def __init__(self, data):
        super().__init__(f"numerical settings", data)


class AggregationSettingsTree(SetttingsTreeBase):

    def __init__(self, data):
        super().__init__(f"numerical settings", data)

    def add_branch(self):
        for inst in self.data:
            _data = inst.to_dict()
            url_path = PurePosixPath(
                unquote(urlparse(_data.pop("url")).path)
            )
            sub_tree = self.tree.add(
                f"[green] aggregation settings [ID {url_path.name}]"
            )
            for field, value in _data.items():
                if field in self.SKIP_FIELDS:
                    continue
                sub_tree.add(f"[blue]{field}: [bold cyan]{value}")


class ResponseTree:

    def __init__(self, resp: SimulationSettingsOverview):
        self.resp = resp
        self.label = Panel(
            f"Settings for simulation {self.resp.general_settings.simulation_id}",
            style="bold green",
            border_style="green",
            title="+++"
        )

    def general_settings(self):
        gt = GeneralSettingsTree(self.resp.general_settings)
        gt.add_branch()
        return gt

    def time_step_settings(self):
        tss = TimeStepSettingsTree(self.resp.time_step_settings)
        tss.add_branch()
        return tss

    def numerical_settings(self):
        ns = NumericalSettingsTree(self.resp.numerical_settings)
        ns.add_branch()
        return ns

    def aggregation_settings(self):
        aggr_sett = AggregationSettingsTree(self.resp.aggregation_settings)
        aggr_sett.add_branch()
        return aggr_sett

    def show(self):
        self.general_settings()
        self.time_step_settings()
        self.numerical_settings()
        t = self.aggregation_settings()
        if not t.tree.label:
            t.tree.label = self.label
        t.show()
