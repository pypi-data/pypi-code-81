"""Create, save and load a stored model."""
from dataclasses import asdict
import toml
from typing import List, Mapping

from aidkitcli.core.stored_model import DataColumn, StoredModel


def load_stored_model(path: str) -> StoredModel:
    """
    Load a stored model.

    :param path: path to the TOML file that contains the model information
    """
    stored_model_dict = toml.load(path)
    stored_model = StoredModel(**stored_model_dict)
    return stored_model


def save_stored_model(stored_model: StoredModel, path: str):
    """
    Save the information about a model in a TOML file.

    :param stored_model: StoredModel dataclass with the model information
    :param path: path where the TOML file is saved
    """
    stored_model_dict = asdict(stored_model)
    with open(path, 'w') as f:
        toml.dump(stored_model_dict, f)


def create_stored_model(checkpoints: List[str],
                        type: List[str],
                        task: List[str],
                        framework: List[str],
                        start_eval: int,
                        prediction_window: int,
                        input: Mapping[str, DataColumn],
                        output: Mapping[str, DataColumn]) -> StoredModel:
    """
    Create a StoredModel instance with all the information needed to perform
    an analysis.

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
    """
    stored_model = StoredModel(checkpoints=checkpoints,
                               type=type,
                               task=task,
                               framework=framework,
                               start_eval=start_eval,
                               prediction_window=prediction_window,
                               input=input,
                               output=output)
    return stored_model
