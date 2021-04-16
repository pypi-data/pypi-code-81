#!/usr/bin/env python3

from codoc.domain.model import Graph
from .high_order_filter import filter_nodes_by_lambda


# TODO this fails if you do an OR on two graphs where node is in both.
def exclude_external(graph: Graph) -> Graph:
    return filter_nodes_by_lambda(lambda node: not node.external)(graph)
