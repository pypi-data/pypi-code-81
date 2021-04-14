"""Create a RequestModel to execute a Gradient Map analysis."""

from aidkitcli.core.analyses.gradient_map import gradient_map as request_factory
from aidkitcli.core.execute_analysis import execute_analysis
from aidkitcli.core.report import Report


def gradient_map(data: str, model: str,
                 title: str = "Config Gradient Map Analysis") -> Report:
    """
    Visualize which inputs affect the model's prediction the most in a plot
    that shows the development of the gradient across the data points.

    When the task addressed by the model is regression, the gradient is
    computed using the predicted value. In case of a classification model,
    the gradient is calculated using the value of the output neuron of
    the class with the highest score.

    The gradient information is rescaled such that the gradient values always
    stay between -1 and 1.

    :param data: name of the data set
    :param model: path to the TOML file that contains the model information
    :param title: title of the configuration (default: "Config Gradient Map
        Analysis")
    """
    request_model = request_factory(
        data=data,
        model=model,
        title=title
    )
    return execute_analysis(request_model=request_model)
