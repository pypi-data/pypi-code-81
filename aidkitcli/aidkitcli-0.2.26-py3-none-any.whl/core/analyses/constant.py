"""Create a RequestModel for a Constant corruption."""
from typing import Union

from aidkitcli.core.utils import create_toml
from aidkitcli.core.request_model import RequestModel
from aidkitcli.data_access.stored_model_access import load_stored_model


def constant(data: str,
             model: str,
             variable_name: str,
             constant: Union[float, str],
             start_index: int = 0,
             perturbation_length: int = 100000,
             title="Config Constant Corruption"
             ) -> RequestModel:
    """
    Create a RequestModel for a Constant Corruption. The execution of this
    request returns a plot showing the performance of the model on the
    corrupted data.

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
    :return: a RequestModel instance containing all the information needed to
        execute a Constant Corruption
    """
    stored_model = load_stored_model(path=model)
    toml_dict = create_toml(
        title=title,
        data=data,
        stored_model=stored_model,
        corruption={"constant": {
            "variable_name": variable_name,
            "constant": constant,
            "start_index": start_index,
            "perturbation_length": perturbation_length,
            "saver": 1
        }}
    )
    return RequestModel(toml_dict)
