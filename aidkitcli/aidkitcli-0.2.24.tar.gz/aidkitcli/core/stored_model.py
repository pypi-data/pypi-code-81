"""Abstract the structure of the model information in our TOML files."""
from dataclasses import dataclass
from typing import List, Mapping, Optional, Union


@dataclass
class DataColumn:
    """
    Data class to store all the relevant information about a data column
    (input feature or output value) of the AI model. In particular, this data
    class informs us how the corresponding data column has to be transformed
    before being handed to or returned by the AI model.

    :param type: type of the data column linked to an input feature or output
        value, each variable can be either quantitative or categorical
    :param processing: name of the data processing function to be used to
        process the values of the data column (e.g. min_max, dummify)
    :param min_value: minimum value of the data column
    :param max_value: maximum value of the data column
    :param discrete: whether the quantitative variable of the data column is
        discrete (only for input features)
    :param categories: list of categories of the data column
    """
    type: str
    processing: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    discrete: Optional[bool] = None
    categories: Optional[List[Union[str, float]]] = None


@dataclass
class StoredModel:
    """
    Data class to store all the information about a model needed to execute an
    analysis.

    :param checkpoints: name of the checkpoint
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
    checkpoints: Union[str, List[str]]
    type: List[str]
    task: List[str]
    framework: List[str]
    input: Mapping[str, DataColumn]
    output: Mapping[str, DataColumn]
    start_eval: Optional[int] = None
    prediction_window: Optional[int] = None
