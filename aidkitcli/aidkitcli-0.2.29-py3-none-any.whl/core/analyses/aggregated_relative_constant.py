"""Create a RequestModel for an Aggregated Relative Constant corruption."""

from aidkitcli.core.utils import create_toml
from aidkitcli.core.request_model import RequestModel
from aidkitcli.data_access.stored_model_access import load_stored_model


def aggregated_relative_constant(data: str,
                                 model: str,
                                 variable_name: str,
                                 start_relative_constant: float,
                                 end_relative_constant: float,
                                 start_index: int = 0,
                                 perturbation_length: int = 100000,
                                 number_of_constants: int = 10,
                                 title="Config Aggregated Relative Constant Corruption"
                                 ) -> RequestModel:
    """
    Create a RequestModel for an Aggregated Relative Constant Corruption. The
    execution of this request returns a plot showing the performance of the
    model on the corrupted data.

    This corruption is an aggregated version of the relative_constant, i.e.
    different relative values equally distributed between
    start_relative_constant and end_relative_constant are added to the
    original value of the selected variable while the resulting average
    absolute errors are tracked.

    This corruption can only be applied to quantitative input variables and
    the ML models supported are Keras regression recurrent models.

    :param data: name of the data set
    :param model: path to the TOML file that contains the model information
    :param variable_name: name of the variable to corrupt
    :param start_relative_constant: starting value of the perturbation
    :param end_relative_constant: maximal value of the corruption that should
        not be surpassed
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    :param number_of_constants: number of constant values to be tested to
        generate the average absolute error plot
    :param title: title of the configuration (default: "Config Aggregated
        Relative Constant Corruption")
    :return: a RequestModel instance containing all the information needed to
        execute an Aggregated Relative Constant Corruption
    """
    stored_model = load_stored_model(path=model)
    toml_dict = create_toml(
        title=title,
        data=data,
        stored_model=stored_model,
        corruption={"aggregated_relative_constant": {
            "variable_name": variable_name,
            "start_relative_constant": start_relative_constant,
            "end_relative_constant": end_relative_constant,
            "start_index": start_index,
            "perturbation_length": perturbation_length,
            "number_of_constants": number_of_constants,
            "saver": 1
        }}
    )
    return RequestModel(toml_dict)
