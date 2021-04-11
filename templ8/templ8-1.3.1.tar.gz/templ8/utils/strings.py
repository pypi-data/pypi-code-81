def quote(string: str) -> str:
    """
    >>> quote('abc')
    '\"abc\"'

    >>> quote('"abc"')
    '\"abc\"'
    """
    return (
        string
        if string.startswith('"') and string.endswith('"')
        else f'"{string}"'
    )


def handle(string: str) -> str:
    """
    >>> handle('https://github.com/user/repo')
    'user/repo'

    >>> handle('user/repo')
    'user/repo'

    >>> handle('')
    ''
    """
    splt = string.split("/")
    return "/".join(splt[-2:] if len(splt) >= 2 else splt)
