#!/usr/bin/env python3
from typing import Set

from codoc.domain.model import Dependency, Node


def get_edges_where_both_ends_are_in_nodes(edges: Set[Dependency], nodes: Set[Node]):
    node_identifiers = set(node.identifier for node in nodes)
    return set(
        edge
        for edge in edges
        if is_both_edges_of_edge_in_list_of_nodes(edge, node_identifiers)
    )


def is_both_edges_of_edge_in_list_of_nodes(
    edge: Dependency, node_identifiers: Set[str]
) -> bool:
    is_from_node_internal = edge.from_node in node_identifiers
    is_to_node_internal = edge.to_node in node_identifiers
    return is_from_node_internal and is_to_node_internal


def is_either_edges_of_edge_in_list_of_nodes(
    edge: Dependency, node_identifiers: Set[str]
) -> bool:
    is_from_node_internal = edge.from_node in node_identifiers
    is_to_node_internal = edge.to_node in node_identifiers
    return is_from_node_internal or is_to_node_internal
