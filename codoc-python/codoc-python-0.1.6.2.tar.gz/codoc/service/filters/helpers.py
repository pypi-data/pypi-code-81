#!/usr/bin/env python3
from codoc.domain.model import Node


def node_without_parent(node: Node) -> Node:
    kwargs = node.__dict__
    kwargs["parent_identifier"] = None
    return Node(**kwargs)
