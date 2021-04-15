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
"""Module for nodes that access attributes of other nodes."""
from typing import (
    Any,
    Dict,
    List,
    Union,
)

import forge

from qctrlcommons.node.base import Node
from qctrlcommons.node.wrapper import NamedNodeData


class GetAttributeNode(Node):
    """
    Gets an attribute from a node value.

    Parameters
    ----------
    value : Any
        The value from which to get the item.
    attr : int or slice or List[int or slice]
        The attribute for the item or items.
    name : str, optional
        The name of the node.

    Returns
    -------
    Any
        The item or items obtained from `value.attr`, or to be more precise,
        ``getattr(value, attr)``.
    """

    name = "getattr"
    args = [
        forge.arg("value"),
        forge.arg("attr", type=str),
    ]

    def _evaluate_node(
        self, execution_context: "ExecutionContext", args: List, kwargs: Dict
    ) -> Any:
        """Evaluate the value of the node by accessing the attribute.

        Parameters
        ----------
        execution_context : ExecutionContext
            helper class for evaluating the value of the node.
        args : List
            argument list for the node.
        kwargs : Dict
            keyword arguments for the Node.

        Returns
        -------
        Any
            the value of the accessible attribute.
        """

        def evaluate(value, attr):
            if not hasattr(value, attr):
                raise AttributeError("missing attribute %s" % attr)
            return getattr(value, attr)

        return evaluate(*args, **kwargs)

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        return NamedNodeData(_operation)


class GetItemNode(Node):
    """
    Gets an item (or items) from a node value.

    Typically you would use slicing syntax ``value[key]`` instead of
    using this function directly.

    Parameters
    ----------
    value : Any
        The value from which to get the item.
    key : int or slice or List[int or slice]
        The key for the item or items.
    name : str, optional
        The name of the node.

    Returns
    -------
    Any
        The item or items obtained from ``value[key]``.
    """

    name = "getitem"
    args = [
        forge.arg("value"),
        forge.arg("key", type=Union[int, slice, List[Union[int, slice]]]),
    ]

    def _evaluate_node(
        self, execution_context: "ExecutionContext", args, kwargs
    ) -> Any:
        # Use an inner function to automatically unpack the args and
        # kwargs into the appropriate named args.
        def evaluate(value, key):
            return value[key]

        return evaluate(*args, **kwargs)

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        return NamedNodeData(_operation)
