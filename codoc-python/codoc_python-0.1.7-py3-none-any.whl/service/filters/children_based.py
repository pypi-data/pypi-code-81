# /usr/bin/env python3
from typing import Set, Union
from codoc.domain.model import Graph, Node, NodeId, Dependency
from codoc.service.parsing.node import get_identifier_of_object
from codoc.domain.helpers import get_node, get_children, set_parent
from .types import FilterType
from .helpers import (
    is_both_edges_of_edge_in_list_of_nodes,
    is_either_edges_of_edge_in_list_of_nodes,
)


def get_children_of(
    node: Union[str, object, Node], keep_external_nodes: bool = False
) -> FilterType:
    """
    :param node: The node, object or string identifier of what to filter based on
    :param keep_external_nodes: Whether to keep external dependencies of children
    :returns: A filter function that excludes non-children
    :rtype: GraphFilter

    Returns a filter that only returns children of the node given via the identifier.

    The returned filter (function) can then be called with a given graph.

    **Important**: Children are **NOT** dependencies, they are things defined inside
    the current node. I.e if a class, Foo, defined in FooModule, then FooModule
    is the parent of Foo.

    Example

    .. code-block:: python

       # returns all modules/classes/exceptions/functions
       # defined inside `myporject.subproject`.

       filter_function = filters.get_children_of(myproject.subproject)

       filtered_graph = filter_function(graph)

    """
    if not isinstance(node, str):
        if isinstance(node, Node):
            identifier = node.identifier
        else:
            identifier = get_identifier_of_object(node)
    else:
        identifier = node

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
                edges=graph.edges,
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
                edges=graph.edges,
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
    if keep_external_nodes:
        return is_either_edges_of_edge_in_list_of_nodes(edge, node_identifiers)
    else:
        return is_both_edges_of_edge_in_list_of_nodes(edge, node_identifiers)


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
