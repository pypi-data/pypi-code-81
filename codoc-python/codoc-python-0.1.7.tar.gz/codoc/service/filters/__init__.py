"""
Filters can be used to filter a graph.

This is used to create a more special and specific view, making it more
viewer friendly.
"""
from .class_diagram import class_diagram_filter
from .children_based import get_children_of
from .depth_based import get_depth_based_filter
from .external_exclusion import exclude_external
from .type_exclusion_filter import (
    exclude_classes,
    exclude_functions,
    exclude_modules,
    exclude_exceptions,
    include_only_classes,
    include_only_functions,
    include_only_modules,
    include_only_exceptions,
)
from .regex_based import filter_by_regex, exclude_by_regex


__all__ = [
    "class_diagram_filter",
    "exclude_classes",
    "exclude_functions",
    "exclude_modules",
    "exclude_exceptions",
    "include_only_classes",
    "include_only_modules",
    "include_only_functions",
    "include_only_exceptions",
    "get_children_of",
    "get_depth_based_filter",
    "exclude_external",
    "filter_by_regex",
    "exclude_by_regex",
]
