#!/usr/bin/env python3
import types

from codoc.domain.model import Dependency, Graph
from codoc.service.parsing.dependency import (
    get_dependency_nodes,
    get_dependency_nodes_with_parents,
)
from codoc.service.dependency_correcting import create_bubbled_dependencies
from codoc.service.parsing.node import create_node_from_object, get_identifier_of_object

from .object_unpacker import recursively_get_all_subobjects_in_object


def create_graph_of_module(
    module: types.ModuleType,
    include_external_dependencies: bool = True,
    strict_mode: bool = True,
) -> Graph:
    all_objects = frozenset(recursively_get_all_subobjects_in_object(module))
    nodes = set(
        node
        for obj in all_objects
        for node in {create_node_from_object(obj, external=False)}
        | get_dependency_nodes_with_parents(
            obj,
            include_external_dependencies=include_external_dependencies,
            strict_mode=strict_mode,
        )
    )
    edges = set(
        Dependency(
            from_node=get_identifier_of_object(obj),
            to_node=dependency.identifier,
        )
        for obj in all_objects
        for dependency in get_dependency_nodes(
            obj,
            include_external_dependencies=include_external_dependencies,
            strict_mode=strict_mode,
        )
    )
    return create_bubbled_dependencies(Graph(nodes=nodes, edges=edges))
