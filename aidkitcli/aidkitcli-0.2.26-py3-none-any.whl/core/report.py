"""Representation of stored Plots & Metrics"""

from dataclasses import dataclass
from typing import List
from aidkitcli.data_access.authentication import get_url

@dataclass
class Plot:
    name: str
    description: str
    url: str


@dataclass
class Metric:
    name: str
    description: str
    value: float


@dataclass
class Report:
    plots: List[Plot]
    metrics: List[Metric]


def dict2report(report_dict: dict) -> Report:
    plot_dicts = report_dict.get('plots', [])
    metric_dicts = report_dict.get('metrics', [])
    plot_models = [
        Plot(
            name=plot['name'],
            description=plot['description'],
            url=get_url() + plot['url']
        )
        for plot in plot_dicts
    ]
    metric_models = [
        Metric(
            name=plot['name'],
            description=plot['description'],
            value=plot['value']
        )
        for plot in metric_dicts
    ]
    report_model = Report(
        plots=plot_models,
        metrics=metric_models
    )
    return report_model
