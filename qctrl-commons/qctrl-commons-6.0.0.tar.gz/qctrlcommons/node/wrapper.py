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
"""Module for all Node wrappers."""
from dataclasses import dataclass
from typing import Any

import pythonflow as pf

from qctrlcommons.exceptions import QctrlGraphIntegrityError


class Operation(pf.Operation):  # pylint:disable=abstract-method
    """
    Version of `pf.Operation` that stores a reference to a named operation.

    Similar to `pf.func_op`, but also performs some validation during initialization to make sure
    that all the argument nodes belong to the same graph.
    """

    def __init__(self, func, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.operation_name = func

        self._iter_validate_op_graph(args)
        self._iter_validate_op_graph(kwargs)

    def _iter_validate_op_graph(self, value: Any) -> None:
        """Validates that `value.graph` (if it exists) is the
        same as `self.graph`. This is to avoid having arguments of type `Operation`
        that belong to a different graph.

        Parameters
        ----------
        value: Any
            One of the args/kwargs passed to the __init__ function.

        Raises
        ------
        QctrlGraphIntegrityError
            In case any of the arguments of the current operations is
            of type `pf.func_op` and belongs to a different instance `pf.Graph`
        """
        if isinstance(value, (list, tuple)):
            for val in value:
                self._iter_validate_op_graph(val)
        elif isinstance(value, dict):
            for val in value.values():
                self._iter_validate_op_graph(val)
        elif isinstance(value, NodeData):
            if self.graph != value.operation.graph:
                raise QctrlGraphIntegrityError(
                    f"{value.operation.name} does not "
                    f"belong to the same graph as {self.name!r}."
                )


@dataclass
class NodeData:
    """
    Base class for information about a created node in a client-side graph.

    Contains information about the corresponding Pythonflow operation, together with type-specific
    validation data.
    """

    operation: Operation


class NameMixin:
    """
    Mixin to be used by nodes whose name can be chosen and accessed by the
    user. That is, the nodes that are fetchable.
    """

    @property
    def name(self):
        """
        Get the name/id of pythonflow operation.
        """
        return self.operation.name

    @name.setter
    def name(self, name):
        self.operation.name = name


@dataclass
class NamedNodeData(NodeData, NameMixin):
    """
    NodeData subclass to be used by basic nodes that also have names.
    """
