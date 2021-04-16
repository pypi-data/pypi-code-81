#!/usr/bin/env python3
from typing import Callable

from codoc.domain.model import Graph, Node

from .types import FilterType


def filter_nodes_by_lambda(filter_function: Callable[[Node], bool]) -> FilterType:
    def internal_filter(graph: Graph) -> Graph:
        nodes = {node for node in graph.nodes if filter_function(node)}
        return Graph(nodes=nodes, edges=graph.edges)

    return internal_filter
