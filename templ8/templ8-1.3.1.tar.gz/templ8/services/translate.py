def lifecycle_stage(key: int) -> str:
    """
    >>> lifecycle_stage(1)
    'Planning'

    >>> lifecycle_stage(0)
    'Unknown'
    """
    levels = {
        1: "Planning",
        2: "Pre-Alpha",
        3: "Alpha",
        4: "Beta",
        5: "Production/Stable",
        6: "Mature",
        7: "Inactive",
    }
    return levels[key] if key in range(1, 7) else "Unknown"


def is_kebab_case(string: str) -> bool:
    """
    >>> is_kebab_case('a-b')
    True

    >>> is_kebab_case('ab')
    False

    >>> is_kebab_case('a--b')
    False

    >>> is_kebab_case('-a-b')
    False

    >>> is_kebab_case('a-b-')
    False
    """
    splt = string.split("-")
    return len(splt) > 1 and "" not in splt


def kebab_to_snake(string: str) -> str:
    """
    >>> kebab_to_snake('a-b')
    'a_b'

    >>> kebab_to_snake('ab')
    'ab'

    >>> kebab_to_snake('a--b')
    'a--b'
    """
    return (
        string.replace("-", "_") if is_kebab_case(string) else string
    )
