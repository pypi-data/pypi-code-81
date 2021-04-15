"""Create a RequestModel for an Increasing - Decreasing corruption."""

from aidkitcli.core.utils import create_toml
from aidkitcli.core.request_model import RequestModel
from aidkitcli.data_access.stored_model_access import load_stored_model


def inc_dec(data: str,
            model: str,
            variable_name: str,
            step_length: int,
            start_constant: float,
            end_constant: float,
            start_index: int = 0,
            perturbation_length: int = 100000,
            title="Config Increasing - Decreasing Corruption"
            ) -> RequestModel:
    """
    Create a RequestModel for an Increasing - Decreasing Corruption. The
    execution of this request returns a plot showing the performance of the
    model on the corrupted data.

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
    stored_model = load_stored_model(path=model)

    if start_constant < end_constant:
        factor = 1.0
    else:
        factor = -1.0

    toml_dict = create_toml(
        title=title,
        data=data,
        stored_model=stored_model,
        corruption={"inc_dec": {
            "variable_name": variable_name,
            "step_length": step_length,
            "start_constant": start_constant,
            "end_constant": end_constant,
            "factor": factor,
            "start_index": start_index,
            "perturbation_length": perturbation_length,
            "saver": 1
        }}
    )
    return RequestModel(toml_dict)
