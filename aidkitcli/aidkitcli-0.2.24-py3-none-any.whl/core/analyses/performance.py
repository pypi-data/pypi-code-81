"""Create a RequestModel for a Performance analysis."""

from aidkitcli.core.utils import create_toml
from aidkitcli.core.request_model import RequestModel
from aidkitcli.data_access.stored_model_access import load_stored_model


def performance(data: str, model: str, report=True,
                title="Config Performance Analysis") -> RequestModel:
    """
    Create a Request Model to measure the accuracy of a model and translate
    it into a plot that shows the performance of the model w.r.t. the data
    set and 3 different metrics, namely mean absolute error, correlation
    coefficient and maximal error.

    In case the task addressed by the model is regression, a plot comparing
    the LSTM to the mathematical model is also displayed.

    The metrics are calculated across all the files within a data folder.

    :param data: name of the data set
    :param model: path to the TOML file that contains the model information
    :param report: whether to create a performance report or not (default:
        True)
    :param title: title of the configuration (default: "Config Performance
        Analysis")
    :return: a RequestModel instance containing all the information needed to
        execute a Performance Analysis
    """
    stored_model = load_stored_model(path=model)
    toml_dict = create_toml(
        title=title,
        data=data,
        stored_model=stored_model,
        performance={"report": report}
    )
    return RequestModel(toml_dict)
