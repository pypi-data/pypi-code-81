"""Create a RequestModel for a Gradient Map analysis."""

from aidkitcli.core.utils import create_toml
from aidkitcli.core.request_model import RequestModel
from aidkitcli.data_access.stored_model_access import load_stored_model


def gradient_map(data: str, model: str,  target_output: int = 0,
                 title: str = "Config Gradient Map Analysis",) -> RequestModel:
    """
    Create a RequestModel to visualize which inputs affect the model's
    prediction the most in a plot that shows the development of the
    gradient across the data points.

    When the task addressed by the model is regression, the gradient is
    computed using the predicted value. In case of a classification model,
    the gradient is calculated using the value of the output neuron of
    the class with the highest score. In the case of a multiregression model,
    the gradient is computed using the predicted value given as
    target_output.

    The gradient information is rescaled such that the gradient values always
    stay between -1 and 1.

    :param data: name of the data set
    :param model: path to the TOML file that contains the model information
    :param target_output: index of the output variable to use for gradient
                          calculation (only relevant for multi-variable
                          regression)
    :param title: title of the configuration (default: "Config Gradient Map
                  Analysis")
    :return: a RequestModel instance containing all the information needed to
        execute a Gradient Map Analysis
    """
    stored_model = load_stored_model(path=model)
    toml_dict = create_toml(
        title=title,
        data=data,
        stored_model=stored_model,
        gradient_map={
            "target_output": target_output
        }
    )
    return RequestModel(toml_dict)
