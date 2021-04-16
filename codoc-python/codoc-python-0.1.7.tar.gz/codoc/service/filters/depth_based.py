#!/usr/bin/env python3
"""
These filters look at the depth of a graph, and
return new graphs that are based on the so-called depth of a given node.

With "depth" we mean how close to the root of a graph it is, i.e
a depth=1 would only take the top-level modules, where depth 2
would take all nodes that are direct children of top-level modules.

Depth can be found by recursively checking if the parent has a parent,
and if yes check that parent too, and return how many steps one has to
 progress before returning a null value.
"""

from codoc.domain.helpers import get_node
from codoc.domain.model import Graph, Node

from .types import FilterType


def get_depth_based_filter(depth: int) -> FilterType:
    def depth_based_filter(graph: Graph) -> Graph:
        nodes = set(
            node for node in graph.nodes if get_depth_of_node(node, graph) <= depth
        )
        return Graph(nodes=nodes, edges=graph.edges)

    return depth_based_filter


def get_depth_of_node(node: Node, graph: Graph) -> int:
    parent_id = node.parent_identifier
    if parent_id is None:
        return 1
    parent = parent_id = get_node(parent_id, graph)
    return get_depth_of_node(parent, graph) + 1
