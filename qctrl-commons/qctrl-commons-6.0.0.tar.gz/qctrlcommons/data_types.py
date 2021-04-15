# Copyright 2020 Q-CTRL Pty Ltd & Q-CTRL Inc. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#     https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.
"""Module for declaring the datatype."""
import base64
from typing import (
    Any,
    Union,
)

import numpy as np
import pythonflow as pf
from scipy.sparse import coo_matrix

from qctrlcommons.graph import Graph
from qctrlcommons.node.registry import (
    NODE_REGISTRY,
    Node,
)
from qctrlcommons.node.wrapper import (
    NodeData,
    Operation,
)


class DataType:
    """Framework for supporting data types which are not JSON serializable by
    default.

    Attributes
    ----------
    _type: Callable
         data type
    object_key: str
        key name for the data
    """

    _type = None
    object_key = None

    def can_encode(self, obj: Any) -> bool:
        """Checks that the object can be encoded with this class. Default
        behaviour is to check that the object is an instance of _type.

        Parameters
        ----------
        obj : Any
            object to be examined.

        Returns
        -------
        bool
            True if the object can be encoded, False otherwise.

        Raises
        ------
        RuntimeError
            if the data type is `None`.
        """
        if self._type is None:
            raise RuntimeError("_type not set for: {}".format(self))

        return isinstance(  # pylint:disable=isinstance-second-argument-not-valid-type
            obj, self._type
        )

    def encode(self, obj) -> dict:
        """Encodes the object. Result should be JSON serializable. To be
        overridden by subclass.

        Parameters
        ----------
        obj : Any
            object to be encoded.
        """
        raise NotImplementedError

    def can_decode(self, obj: dict) -> bool:
        """Checks that the object can be decoded with this class. Default
        behaviour is to check that the object_key exists in the object.

        Parameters
        ----------
        obj : Any
            object to be examined.

        Returns
        -------
        bool
            True if the object can be decoded, False otherwise.

        Raises
        ------
        RuntimeError
            if `object_key` is `None`.
        """
        if self.object_key is None:
            raise RuntimeError("object_key not set for: {}".format(self))

        return self.object_key in obj

    def decode(self, obj: dict):
        """Decodes the object. To be overridden by subclass.

        Parameters
        ----------
        obj: dict
            object to be decoded.
        """
        raise NotImplementedError


class SliceDataType(DataType):
    """Handle slice serialization."""

    _type = slice
    object_key = "encoded_slice"

    def encode(self, obj: slice) -> dict:
        return {
            self.object_key: True,
            "start": obj.start,
            "stop": obj.stop,
            "step": obj.step,
        }

    def decode(self, obj: dict) -> slice:
        return slice(obj.get("start"), obj.get("stop"), obj.get("step"))


class NumpyScalar(DataType):  # pylint:disable=abstract-method
    """Handle np.number serialization."""

    _type = np.number

    def encode(self, obj: np.number) -> Any:
        """cast to python builtin int or float"""
        return obj.item()

    def can_decode(self, obj: dict) -> bool:
        return False


class NumpyArray(DataType):
    """Represent NumpyArray Model."""

    _type = np.ndarray
    object_key = "base64_encoded_array"

    def encode(self, obj):
        if obj.flags["C_CONTIGUOUS"]:
            obj_data = obj.data
        else:
            cont_obj = np.ascontiguousarray(obj)
            assert cont_obj.flags[  # pylint:disable=unsubscriptable-object
                "C_CONTIGUOUS"
            ]
            obj_data = cont_obj.data

        data_b64 = base64.b64encode(obj_data)
        return {
            self.object_key: data_b64.decode("ascii"),
            "dtype": str(obj.dtype),
            "shape": list(obj.shape),
        }

    def decode(self, obj):
        return np.frombuffer(
            base64.b64decode(obj[self.object_key]), dtype=obj["dtype"]
        ).reshape(obj["shape"])


class NumpyComplexNumber(DataType):
    """Represent NumpyComplexNumber Model."""

    _type = np.complexfloating
    object_key = "base64_encoded_data"

    def encode(self, obj) -> dict:
        obj_data = obj.data
        data_b64 = base64.b64encode(obj_data)
        return {
            self.object_key: data_b64.decode("utf-8"),
            "dtype": str(obj.dtype),
            "shape": list(obj.shape),
        }

    def decode(self, obj: dict):
        cast_to = getattr(np, obj["dtype"])
        return cast_to(
            np.frombuffer(
                base64.b64decode(obj[self.object_key]), dtype=obj["dtype"]
            ).reshape(obj["shape"])
        )


class SparseMatrix(DataType):
    """Represent SparseMatrix Model."""

    _type = coo_matrix
    object_key = "encoded_coo_matrix"

    def encode(self, obj) -> dict:
        return {
            self.object_key: {
                "data": obj.data,
                "row": obj.row,
                "col": obj.col,
            },
            "dtype": str(obj.dtype),
            "shape": list(obj.shape),
        }

    def decode(self, obj: dict) -> coo_matrix:
        return coo_matrix(
            (
                obj[self.object_key]["data"],
                (obj[self.object_key]["row"], obj[self.object_key]["col"]),
            ),
            shape=obj["shape"],
            dtype=obj["dtype"],
        )


class ComplexNumber(DataType):
    """Represents ComplexNumber Model."""

    _type = complex
    object_key = "encoded_complex"

    def encode(self, obj) -> dict:
        return {self.object_key: True, "real": obj.real, "imag": obj.imag}

    def decode(self, obj: dict):
        return complex(obj["real"], obj["imag"])


class GraphDataType(DataType):
    """Represent GraphDataType for pythonflow Graph."""

    _type = pf.core.Graph
    object_key = "pythonflow_graph"

    def _parse_kwargs(self, operations, kwarg_value: dict):
        """
        Handles the different kwargs values.
        """

        if isinstance(kwarg_value, dict) and "_kwarg_type" in kwarg_value:
            return operations[kwarg_value["value"]]

        if isinstance(kwarg_value, dict):
            return {
                key: self._parse_kwargs(operations, kwarg_value[key])
                for key in kwarg_value
            }

        if isinstance(kwarg_value, list):
            return [self._parse_kwargs(operations, value) for value in kwarg_value]

        return kwarg_value

    def _rebuild_operations(self, operations: dict):
        """
        Checks operations to see if any special reference nodes are present.
        If present it repalces them with the real node values.
        """
        # pylint:disable=protected-access
        for operation in operations.values():
            operation._kwargs.update(self._parse_kwargs(operations, operation._kwargs))
        # pylint:enable=protected-access

        return operations

    def encode(self, obj: Union[pf.Graph, Graph]) -> dict:
        """Convert pythonflow graph to dict, all the operations from graph will
        be encoded with OpeationDataType.

        Parameters
        ----------
        obj: Union[pf.Graph, Graph]
            object to be encoded.

        Returns
        -------
        dict
            serialized graph.
        """
        return {
            self.object_key: True,
            "operations": obj.operations,
            "dependencies": obj.dependencies,
        }

    def decode(self, obj: dict) -> Graph:
        """Decode to pythonflow graph.

        Parameters
        ----------
        obj: dict
            object to be decoded.

        Returns
        -------
        Graph
            a custom structure for encoding and decoding pythonflow graph.

        Raises
        ------
        KeyError
            if there's no `operations` in the graph.
        """
        if not obj.get("operations", None):
            raise KeyError("Missing operations. It cannot be encoded to graph")

        operations = self._rebuild_operations(obj["operations"])
        return Graph(operations, obj["dependencies"])

    def can_encode(self, obj) -> bool:
        return isinstance(obj, (pf.core.Graph, Graph))


class OperationDataType(DataType):
    """
    Wrapper class for pythonflow operation.
    """

    _type = Operation
    object_key = "pythonflow_op"

    def _set_kwargs_reference(self, value: Any):
        """
        Checks which kwargs contain values that represent NodeData and stores only the references
        for those values.
        """
        if isinstance(value, NodeData):
            return {"_kwarg_type": "NodeData", "value": value.operation.name}

        if isinstance(value, Node):
            return {"_kwarg_type": "Node", "value": value.node_id}

        if isinstance(value, list):
            return [self._set_kwargs_reference(input) for input in value]

        if isinstance(value, dict):
            return {key: self._set_kwargs_reference(value[key]) for key in value}

        return value

    def encode(self, obj) -> dict:

        if isinstance(obj, Node):
            obj_id = obj.node_id
            operation_name = obj.name
            kwargs = self._set_kwargs_reference(
                obj._kwargs  # pylint:disable=protected-access
            )

        elif isinstance(obj, Operation):
            obj_id = obj.name
            operation_name = obj.operation_name
            kwargs = self._set_kwargs_reference(obj.kwargs)

        else:
            return self.encode(obj.operation)

        return {
            self.object_key: True,
            "id": obj_id,
            "operation_name": operation_name,
            "kwargs": kwargs,
        }

    def decode(self, obj: dict):
        node_cls = NODE_REGISTRY.get_node_cls(obj["operation_name"])
        return node_cls(obj["id"], obj.get("args", []), obj["kwargs"])

    def can_encode(self, obj: Any) -> bool:
        return isinstance(obj, (Operation, NodeData, Node))
