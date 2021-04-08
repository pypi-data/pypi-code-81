"""Create a RequestModel to execute a Random corruption."""

from typing import Dict

from aidkitcli.core.analyses.random import random as request_factory
from aidkitcli.data_access.analysis import post_analysis


def random(data: str,
           model: str,
           variable_name: str,
           step_length: int,
           lower_bound: float,
           upper_bound: float,
           start_index: int = 0,
           perturbation_length: int = 100000,
           title: str = "Config Random Corruption"
           ) -> Dict[str, int]:
    """
    Execute a Random Corruption and return a plot showing the performance of
    the model on the corrupted data.

    The values of the selected variable are set to random values sampled from
    a uniform distribution within the fixed range [lower_bound, upper_bound].

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
    :param lower_bound: minimal corruption value which should not be surpassed
    :param upper_bound: maximal corruption value which should not be surpassed
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    :param title: title of the configuration (default: "Config Random
        Corruption")
    """
    request_model = request_factory(
        title=title,
        data=data,
        model=model,
        variable_name=variable_name,
        step_length=step_length,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        start_index=start_index,
        perturbation_length=perturbation_length,
    )
    return post_analysis(request_model=request_model)
