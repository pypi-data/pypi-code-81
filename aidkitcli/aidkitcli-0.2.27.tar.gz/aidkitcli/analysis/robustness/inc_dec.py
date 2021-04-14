"""Create a RequestModel to execute an Increasing - Decreasing corruption."""
from typing import Dict

from aidkitcli.core.analyses.inc_dec import inc_dec as request_factory
from aidkitcli.data_access.analysis import post_analysis


def inc_dec(data: str,
            model: str,
            variable_name: str,
            step_length: int,
            start_constant: float,
            end_constant: float,
            start_index: int = 0,
            perturbation_length: int = 100000,
            title: str = "Config Increasing - Decreasing Corruption"
            ) -> Dict[str, int]:
    """
    Execute an Increasing - Decreasing Corruption and return a plot showing
    the performance of the model on the corrupted data.

    The values of the selected variable are first set to the start_constant
    value and then changed every step_length data points in the file.
    Depending on whether end_constant is bigger or smaller than
    start_constant, the values are increased or decreased after step_length
    data points.

    This corruption can only be applied to quantitative input variables. The
    supported ML models are:

    - Keras regression recurrent models
    - Keras classification feedforward models
    - scikit-learn classification feedforward models

    :param data: name of the data set
    :param model: path to the TOML file that contains the model information
    :param variable_name: name of the variable to corrupt
    :param step_length: number of data points with a constant value before
        the next increase/decrease
    :param start_constant: starting value of the perturbation
    :param end_constant: maximal corruption value that should not be surpassed
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    :param title: title of the configuration (default: "Config Increasing -
        Decreasing Corruption")
    :return: a RequestModel instance containing all the information needed to
        execute an Increasing - Decreasing Corruption
    """
    request_model = request_factory(
        title=title,
        data=data,
        model=model,
        variable_name=variable_name,
        step_length=step_length,
        start_constant=start_constant,
        end_constant=end_constant,
        start_index=start_index,
        perturbation_length=perturbation_length,
    )
    return post_analysis(request_model=request_model)
