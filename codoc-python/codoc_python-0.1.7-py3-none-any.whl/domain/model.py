#!/usr/bin/env python3
"""
The domain model is a conceptual model of the domain that incorporates both behavior and data.

We use it to define the core data classes that are used throughout the project.
"""
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Set, Tuple, Any


class NodeType(Enum):
    CLASS = auto()
    FUNCTION = auto()
    MODULE = auto()
    EXCEPTION = auto()


NodeId = str


@dataclass(frozen=True)
class Node:
    """
    Nodes represents a given source code item,
    i.e a class, function or module.

    It contains all the meta data as well as the code that
    defined the node in question.
    """

    identifier: NodeId
    name: str
    of_type: NodeType
    path: Optional[str]
    args: Optional[Tuple[str, ...]]
    lines: Optional[Tuple[int, int]]
    external: bool = True
    description: Optional[str] = None
    parent_identifier: Optional[NodeId] = None

    def __str__(self) -> str:
        if self.of_type is NodeType.MODULE:
            return self.name

        return f"[Node: {self.name} - {self.of_type} ({self.identifier})]"

    def __hash__(self) -> int:
        return hash(self.identifier)

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        if isinstance(other, Node):
            return self.identifier == other.identifier
        return NotImplemented


@dataclass(frozen=True)
class Dependency:
    """
    A Dependency shows that one node depends on another.
    Currently it doesn't specify the type of dependency.
    """

    from_node: NodeId
    to_node: NodeId

    def __hash__(self) -> int:
        return hash(hash(self.from_node) + hash(self.to_node))


@dataclass(frozen=True)
class Graph:
    """
    A Graph is the base element of the system.
    It contains both edges (Dependencies) as well as nodes (classes, functions, etc).

    It supports a variety of operators.
    """

    edges: Set[Dependency]
    nodes: Set[Node]

    def __and__(self, other: Any) -> "Graph":
        if isinstance(other, Graph):
            nodes = self.nodes & other.nodes
            edges = {
                edge
                for edge in self.edges | other.edges
                if edge_is_in_nodes(edge, nodes)
            }
            return Graph(
                edges=edges,
                nodes=nodes,
            )
        return NotImplemented

    # TODO handle if you have the "external" flag, and one is, the other isn't.
    def __or__(self, other: Any) -> "Graph":
        if isinstance(other, Graph):
            return Graph(edges=self.edges | other.edges, nodes=self.nodes | other.nodes)
        return NotImplemented

    def __xor__(self, other: Any) -> "Graph":
        if isinstance(other, Graph):
            nodes = self.nodes ^ other.nodes
            edges = {
                edge
                for edge in self.edges | other.edges
                if edge_is_in_nodes(edge, nodes)
            }
            return Graph(
                edges=edges,
                nodes=nodes,
            )
        return NotImplemented

    def __sub__(self, other: Any) -> "Graph":
        if isinstance(other, Graph):
            nodes = self.nodes - other.nodes
            edges = {
                edge
                for edge in self.edges | other.edges
                if edge_is_in_nodes(edge, nodes)
            }
            return Graph(
                edges=edges,
                nodes=nodes,
            )
        return NotImplemented


def edge_is_in_nodes(edge: Dependency, nodes: Set[Node]) -> bool:
    return identifier_is_in_nodes(edge.from_node, nodes) and identifier_is_in_nodes(
        edge.to_node, nodes
    )


def identifier_is_in_nodes(identifier: NodeId, nodes: Set[Node]) -> bool:
    return any(identifier == node.identifier for node in nodes)
