"""Create a RequestModel to execute an Aggregated Constant corruption."""

from typing import Dict

from aidkitcli.core.analyses.aggregated_constant import aggregated_constant as request_factory
from aidkitcli.data_access.analysis import post_analysis


def aggregated_constant(data: str,
                        model: str,
                        variable_name: str,
                        start_constant: float,
                        end_constant: float,
                        start_index: int = 0,
                        perturbation_length: int = 100000,
                        number_of_constants: int = 10,
                        title: str = "Config Aggregated Constant Corruption"
                        ) -> Dict[str, int]:
    """
    Execute an Aggregated Constant Corruption and return a plot showing the
    performance of the model on the corrupted data.

    This corruption is an aggregated version of the constant corruption, i.e.
    the values of the selected variable are set to different constant values
    starting with start_constant and equally distributed till end_constant
    while the resulting average absolute errors of the model are tracked.

    This corruption is an aggregated version of the constant corruption, i.e.
    the values of the selected variable are set to different constant values
    starting with start_constant and equally distributed till end_constant
    while the resulting average absolute errors of the model are tracked.

    This corruption can only be applied to quantitative input variables. The
    supported ML models are:

    - Keras regression recurrent models
    - Keras classification feedforward models
    - scikit-learn classification feedforward models

    :param data: name of the data set
    :param model: path to the TOML file that contains the model information
    :param variable_name: name of the variable to corrupt
    :param start_constant: first value the chosen variable is set to
    :param end_constant: maximal corruption value that should not be surpassed
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    :param number_of_constants: number of constant values to be tested to
        generate the average absolute error plot
    :param title: title of the configuration (default: "Config Aggregated
        Constant Corruption")
    """
    request_model = request_factory(
        title=title,
        data=data,
        model=model,
        variable_name=variable_name,
        start_constant=start_constant,
        end_constant=end_constant,
        start_index=start_index,
        perturbation_length=perturbation_length,
        number_of_constants=number_of_constants,
    )
    return post_analysis(request_model=request_model)
