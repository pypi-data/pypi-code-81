import lumipy.ml.onnx.sklearn_to_onnx as onnx
from onnx.onnx_ml_pb2 import ModelProto
from typing import Union
from sklearn.base import BaseEstimator, TransformerMixin
from pandas import DataFrame
from numpy import ndarray


def sklearn_to_onnx(model: Union[BaseEstimator, TransformerMixin], data: Union[DataFrame, ndarray]) -> ModelProto:
    """Convert an sklearn transformer, estimator or pipeline to ONNX graph (ModelProto).

    Args:
        model (Union[BaseEstimator, TransformerMixin]): sklearn estimator, transformer or pipeline to convert.
        data (Union[DataFrame, ndarray]): data that the model was trained on - used to determine the input tensor
        schema.

    Returns:
        ModelProto: the resulting ONNX graph object.
    """
    return onnx.sklearn_to_onnx(model, data)
