# /usr/bin/env python3
from typing import Set
from codoc.domain.model import Graph, Node, NodeId, Dependency
from codoc.domain.helpers import get_node, get_children, set_parent
from .types import FilterType


def get_children_of(identifier: str, keep_external_nodes: bool = False) -> FilterType:
    """
    :param identifier: The string identifier of the parent class we want children of
    :param keep_external_nodes: Whether to keep external dependencies of children
    :returns: A filter function that excludes non-children
    :rtype: GraphFilter

    Returns a filter that only returns children of the node given via the identifier.

    The returned filter (function) can then be called with a given graph.

    Example

    .. code-block:: python

        from codoc.service.parsing.node import get_identifier_of_object

       identifier = get_identifier_of_object(myproject.subproject)
       filter_function = get_children_of(identifier)

       filtered_graph = filter_function(graph)



    """
    if not isinstance(identifier, str):
        raise TypeError(f"Identifier has to be a str, was a {type(identifier)}")

    def filter_func(graph: Graph) -> Graph:
        internal_nodes = {
            node for node in graph.nodes if is_node_accepted(node, graph, identifier)
        }
        internal_node_identifiers = {node.identifier for node in internal_nodes}
        edges = {
            edge
            for edge in graph.edges
            if is_edge_accepted(edge, internal_node_identifiers, keep_external_nodes)
        }
        if not keep_external_nodes:
            return Graph(
                nodes={
                    remove_parent_if_parent_is_discarded(
                        node, internal_node_identifiers
                    )
                    for node in internal_nodes
                },
                edges=edges,
            )
        else:
            # Also remove `parent_id` for all nodes if parent_id is outside.
            # TODO keep parent if child is in graph
            return Graph(
                nodes={
                    remove_parent_if_parent_is_discarded(node, internal_nodes)
                    for node in graph.nodes
                    if is_node_in_edges(node, edges, graph)
                    or is_node_accepted(node, graph, identifier)
                },
                edges=edges,
            )

    return filter_func


def remove_parent_if_parent_is_discarded(
    node: Node, node_identifiers: Set[str]
) -> Node:
    parent_id = node.parent_identifier
    if parent_id is not None and parent_id not in node_identifiers:
        return set_parent(node, None)
    return node


# TODO find a way to cache result, i.e dynamic programming
# TODO test these functions individually
def is_node_accepted(node: Node, graph: Graph, allowed_identifier: NodeId) -> bool:
    if node.identifier == allowed_identifier:
        return True

    parent_id = node.parent_identifier
    if not parent_id:
        return False

    parent = get_node(node.parent_identifier, graph)

    return is_node_accepted(parent, graph, allowed_identifier)


def is_edge_accepted(
    edge: Dependency, node_identifiers: Set[str], keep_external_nodes: bool
) -> bool:
    is_from_node_internal = edge.from_node in node_identifiers
    is_to_node_internal = edge.to_node in node_identifiers
    if keep_external_nodes:
        return is_from_node_internal or is_to_node_internal
    else:
        return is_from_node_internal and is_to_node_internal


def is_node_in_edges(node: Node, edges: Set[Dependency], graph: Graph) -> bool:
    is_in_edges = any(
        node.identifier in [edge.from_node, edge.to_node] for edge in edges
    )

    if is_in_edges:
        return True
    # we need to check if a child is here, because then we want to keep the package
    children = get_children(node.identifier, graph)

    if not children:
        return False

    return any(is_node_in_edges(child, edges, graph) for child in children)
