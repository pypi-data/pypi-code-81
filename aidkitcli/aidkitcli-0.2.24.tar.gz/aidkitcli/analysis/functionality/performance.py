"""Create a RequestModel to execute a Performance analysis."""

from typing import Dict

from aidkitcli.core.analyses.performance import performance as request_factory
from aidkitcli.data_access.analysis import post_analysis


def performance(data: str, model: str, report=True,
                title: str = "Config Performance Analysis") -> Dict[str, int]:
    """
    Measure the accuracy of a model and translate it into a plot that shows
    the performance of the model w.r.t. the data set and 3 different metrics,
    namely mean absolute error, correlation coefficient and maximal error.

    In case the task addressed by the model is regression, a plot comparing
    the LSTM to the mathematical model is also displayed.

    The metrics are calculated across all the files within a data folder.

    :param data: name of the data set
    :param model: path to the TOML file that contains the model information
    :param report: whether to create a performance report or not (default:
        True)
    :param title: title of the configuration (default: "Config Performance
        Analysis")
    """
    request_model = request_factory(
        title=title,
        data=data,
        model=model,
        report=report
    )
    return post_analysis(request_model=request_model)
