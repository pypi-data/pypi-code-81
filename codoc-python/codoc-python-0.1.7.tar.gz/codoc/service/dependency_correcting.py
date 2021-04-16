#!/usr/bin/env python3
"""
With dependency bubbling, we mean that any dependency
of a child node is also a dependency of the parent.

Simple example:
You have a graph with 4 nodes
A, B, C, D

B is a child of A
D is a child of C

If there is a dependency between B->D,
then by bubbling the dependencies, we will
also create dependencies between
A->C, A->D, B->C


"""
from typing import Set
from codoc.domain.helpers import get_node
from codoc.domain.model import Graph, Node, Dependency, NodeId


def create_bubbled_dependencies(graph: Graph) -> Graph:

    edges = set(
        edge
        for original_edge in graph.edges
        for edge in _get_edge_superset(original_edge, graph)
    )
    return Graph(nodes=graph.nodes, edges=edges)


def _get_edge_superset(edge: Dependency, graph: Graph):
    parents_of_from_node = _get_set_of_all_parents(edge.from_node, graph)
    parents_of_to_node = _get_set_of_all_parents(edge.to_node, graph)

    return set(
        Dependency(from_node=from_node.identifier, to_node=to_node.identifier)
        for from_node in parents_of_from_node
        for to_node in parents_of_to_node
    )


def _get_set_of_all_parents(identifier: NodeId, graph: Graph) -> Set[Node]:
    node = get_node(identifier, graph)
    parent_id = node.parent_identifier

    if parent_id is None:
        return {node}

    return _get_set_of_all_parents(parent_id, graph) | {node}


def remove_non_connected_edges(graph: Graph) -> Graph:
    node_identifiers = set(node.identifier for node in graph.nodes)
    edges = set(
        edge
        for edge in graph.edges
        if is_both_edges_of_edge_in_list_of_nodes(edge, node_identifiers)
    )
    return Graph(nodes=graph.nodes, edges=edges)


def is_both_edges_of_edge_in_list_of_nodes(
    edge: Dependency, node_identifiers: Set[str]
) -> bool:
    is_from_node_internal = edge.from_node in node_identifiers
    is_to_node_internal = edge.to_node in node_identifiers
    return is_from_node_internal and is_to_node_internal
