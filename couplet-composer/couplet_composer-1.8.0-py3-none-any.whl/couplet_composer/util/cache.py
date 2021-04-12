# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""This utility module has caching utilities."""

from functools import update_wrapper


__all__ = ["cached"]


def cached(func):
    """Decorator that caches result of method or function."""
    cache = {}

    def wrapper(*args, **kwargs):
        key = tuple(args) + tuple(kwargs.items())
        if key not in cache:
            result = func(*args, **kwargs)
            cache[key] = result
            return result
        else:
            return cache[key]
    return update_wrapper(wrapper, func)
