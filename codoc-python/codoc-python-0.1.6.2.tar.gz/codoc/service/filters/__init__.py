"""
Filters can be used to filter a graph.

This is used to create a more special and specific view, making it more
viewer friendly.
"""
from .class_diagram import class_diagram_filter
from .children_based import get_children_of
from .type_exclusion_filter import exclude_classes, exclude_functions, exclude_modules


__all__ = [
    "class_diagram_filter",
    "exclude_classes",
    "exclude_functions",
    "exclude_modules",
    "get_children_of",
]
