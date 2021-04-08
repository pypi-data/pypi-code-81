from dataclasses import asdict
from typing import List, Mapping

from aidkitcli.core.stored_model import DataColumn, StoredModel
from aidkitcli.data_access.stored_model_access import create_stored_model, save_stored_model


def create_toml(title: str, data: str, stored_model: StoredModel, **kwargs) -> dict:
    """
    Create a dictionary with the structure of the config TOML files and
    the information needed to run an analysis.

    :param title: title of the configuration
    :param data: name of the data set
    :param stored_model: StoredModel dataclass with the model information
    :param kwargs: additional keyword arguments related to the analyses
    :return: dictionary containing the information needed to run an analysis
    """
    toml_dict = dict()
    toml_dict["title"] = title
    toml_dict["data"] = list(data.split())
    toml_dict["model"] = asdict(stored_model)
    toml_dict["analyses"] = {**kwargs}
    return toml_dict


def store_model(checkpoints: List[str],
                type: List[str],
                task: List[str],
                framework: List[str],
                start_eval: int,
                prediction_window: int,
                input: Mapping[str, DataColumn],
                output: Mapping[str, DataColumn],
                path: str):
    """
    Create a StoredModel instance and store it as a TOML file at a
    specified location.

    :param checkpoints: list of checkpoints
    :param type: feedforward or recurrent
    :param task: classification or regression
    :param framework: keras or scikit
    :param start_eval: index of first data point to be used for evaluations
    :param prediction_window: number of predictions to be aggregated by mean
        calculation
    :param DataColumn input: dictionary where each key is the name of an
        input column and each value is a DataColumn data class
    :param DataColumn output: dictionary where each key is the name of an
        output column and each value is a DataColumn data class
    :param path: path where the TOML file is saved
    """
    stored_model = create_stored_model(
        checkpoints=checkpoints,
        type=type,
        task=task,
        framework=framework,
        start_eval=start_eval,
        prediction_window=prediction_window,
        input=input,
        output=output
    )

    save_stored_model(stored_model=stored_model, path=path)
