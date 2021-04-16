#!/usr/bin/env python3
"""
Filters that excludes a given node based on the type it is.
It will also remove all dependencies (edges) that reach a node that should be excluded


i.e exclude_modules will return a new graph with all module nodes have been removed.
"""
from codoc.domain.model import Graph, Node, NodeType, Dependency
from codoc.domain.helpers import get_node, set_parent

# TODO we need to remove invalid edges here somehwere.
# Maybe we remove shitty edges at the end.


def include_only_modules(graph: Graph) -> Graph:
    """
    Returns a graph that only has modules
    """
    return TypeBasedFilter(NodeType.MODULE, exclusive=False).filter(graph)


def include_only_functions(graph: Graph) -> Graph:
    """
    Returns a graph that only has functions
    """
    return TypeBasedFilter(NodeType.FUNCTION, exclusive=False).filter(graph)


def include_only_classes(graph: Graph) -> Graph:
    """
    Returns a graph that only has classes
    """
    return TypeBasedFilter(NodeType.CLASS, exclusive=False).filter(graph)


def include_only_exceptions(graph: Graph) -> Graph:
    """
    Returns a graph that only has exceptions
    """
    return TypeBasedFilter(NodeType.EXCEPTION, exclusive=False).filter(graph)


def exclude_modules(graph: Graph) -> Graph:
    """
    Returns a graph that doesn't have any modules
    """
    return TypeBasedFilter(NodeType.MODULE).filter(graph)


def exclude_functions(graph: Graph) -> Graph:
    """
    Returns a graph that doesn't have any functions
    """
    return TypeBasedFilter(NodeType.FUNCTION).filter(graph)


def exclude_classes(graph: Graph) -> Graph:
    """
    Returns a graph that doesn't have any classes
    """
    return TypeBasedFilter(NodeType.CLASS).filter(graph)


def exclude_exceptions(graph: Graph) -> Graph:
    """
    Returns a graph that doesn't have any exceptions
    """
    return TypeBasedFilter(NodeType.EXCEPTION).filter(graph)


class TypeBasedFilter:
    """
    Filters graphs based on the defined type.
    """

    # TODO make this inclusive too

    def __init__(self, based_on_type: NodeType, exclusive: bool = True):
        self._type = based_on_type
        self._exclusive = exclusive

    def filter(self, graph: Graph) -> Graph:
        return Graph(
            edges=graph.edges,
            nodes=set(
                self.node_without_parent_of_type(node, graph)
                for node in graph.nodes
                if self.permitted(node)
            ),
        )

    def node_without_parent_of_type(self, node: Node, graph) -> Node:
        if node.parent_identifier and self.identifier_is_permitted(
            node.parent_identifier, graph
        ):
            return set_parent(node, None)
        return node

    def identifier_is_permitted(self, identifier: str, graph) -> bool:
        return self.permitted(get_node(identifier, graph))

    def permitted(self, node: Node) -> bool:
        return (node.of_type is self._type) ^ self._exclusive
