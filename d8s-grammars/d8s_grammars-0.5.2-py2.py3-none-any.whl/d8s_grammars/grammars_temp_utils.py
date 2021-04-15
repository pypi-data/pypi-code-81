def list_flatten(list_arg: list, level: int = None, **kwargs) -> list:
    """Flatten all items in the list_arg so that they are all items in the same list."""
    import more_itertools

    return list(more_itertools.collapse(list_arg, levels=level, **kwargs))
