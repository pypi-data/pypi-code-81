"""Create a RequestModel to execute a Constant corruption."""
from typing import Union

from typing import Dict

from aidkitcli.core.analyses.constant import constant as request_factory
from aidkitcli.data_access.analysis import post_analysis


def constant(data: str,
             model: str,
             variable_name: str,
             constant: Union[float, str],
             start_index: int = 0,
             perturbation_length: int = 100000,
             title: str = "Config Constant Corruption"
             ) -> Dict[str, int]:
    """
    Execute a Constant Corruption and return a plot showing the performance of
    the model on the corrupted data.

    The values of the selected variable are replaced with a constant value
    given by the constant parameter.

    This corruption can be applied to both quantitative and categorical input
    variables. The supported ML models are:

    - Keras regression recurrent models
    - Keras classification feedforward models
    - scikit-learn classification feedforward models

    :param data: name of the data set
    :param model: path to the TOML file that contains the model information
    :param variable_name: name of the variable to corrupt
    :param constant: constant value of the perturbation
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    :param title: title of the configuration (default: "Config Constant
        Corruption")
    """
    request_model = request_factory(
        title=title,
        data=data,
        model=model,
        variable_name=variable_name,
        constant=constant,
        start_index=start_index,
        perturbation_length=perturbation_length,
    )
    return post_analysis(request_model=request_model)
