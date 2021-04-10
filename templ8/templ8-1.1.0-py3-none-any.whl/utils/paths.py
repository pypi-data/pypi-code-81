import os
from pathlib import Path


def path_head(path: str) -> str:
    """
    Get the head of a path string.

    >>> path_head('/dir1/dir2/path.ext')
    'path.ext'

    Args:
        path (str): Path string.

    Returns:
        str: Path string's head.
    """
    return os.path.split(path)[1]


def path_tail(path: str) -> str:
    """
    Get the tail of a path string.

    >>> path_tail('/dir1/dir2/path.ext')
    '/dir1/dir2'

    Args:
        path (str): Path string.

    Returns:
        str: Path string's tail.
    """
    return os.path.split(path)[0]


def path_base(path: str) -> str:
    """
    Get the base of a path string.

    >>> path_base('/dir1/dir2/path.ext')
    ''

    >>> path_base('dir1/dir2/path.ext')
    'dir1'

    Args:
        path (str): Path string.

    Returns:
        str: Path string's base.
    """

    return os.path.normpath(path).split(os.sep)[0]


def path_ext(path: str) -> str:
    """
    Get the extension of a path string.

    >>> path_ext('/dir1/dir2/path.ext')
    '.ext'

    >>> path_ext('/dir1/dir2/path.ext.j2')
    '.j2'

    Args:
        path (str): Path string.

    Returns:
        str: Path string's extension.
    """
    return os.path.splitext(path)[1]


def replace_head(path: str, head: str) -> str:
    """
    >>> replace_head('original', 'replacement')
    'replacement'

    >>> replace_head('folder/original', 'replacement')
    'folder/replacement'
    """
    return os.path.join(path_tail(path), head)


def replace_tail(path: str, search: str, replace: str) -> str:
    """
    >>> replace_tail('/dir1/dir2/path.ext', '/dir1', '/dir2')
    'dir2/dir2/path.ext'

    >>> replace_tail('/dir1/dir2/path.ext', '/dir1/', '/dir2/')
    'dir2/dir2/path.ext'

    >>> replace_tail('/dir1/dir2/path.ext', '/dir3', '/dir2')
    '/dir1/dir2/path.ext'
    """
    # Ensure the search path has a trailing slash
    search = os.path.join(search, "")

    # Ensure the search path has a trailing slash and no leading slash
    replace = os.path.join(replace, "")
    replace = (
        replace[1:] if replace.startswith(os.path.sep) else replace
    )

    return (
        path.replace(search, replace, 1)
        if path.startswith(search)
        else path
    )


def trim_tail(path: str, search: str) -> str:
    """
    >>> trim_tail('/dir1/dir2/path.ext', '/dir1')
    'dir2/path.ext'

    >>> trim_tail('/dir1/dir2/path.ext', '/dir1/')
    'dir2/path.ext'

    >>> trim_tail('/dir1/dir2/path.ext', '/dir3')
    '/dir1/dir2/path.ext'
    """
    return replace_tail(path, search, "")


def replace_ext(path: str, ext: str) -> str:
    """
    Replace a path's extension with another.

    >>> replace_ext('/dir1/dir2/path.ext', '.ext2')
    '/dir1/dir2/path.ext2'

    Args:
        path (str): Path string.
        ext (str): New extension.

    Returns:
        str: Path string with new extension.
    """
    return path.replace(os.path.splitext(path)[1], ext)


def create_parents(path: str) -> None:
    """
    Create a path's parent directories.

    Args:
        path (str): Path string.
    """
    Path(path_tail(path)).mkdir(parents=True, exist_ok=True)


def reverse_to_root(project_root: str, output_dir: str) -> str:
    """

    Get the relative path required to move to a project's root from some output
    directory.

    >>> reverse_to_root('/dir1/dir2', '/dir1/dir3')
    '../dir2'

    Args:
        project_root (str): Root path string.
        output_dir (str): Directory path string.

    Returns:
        str: Path string.
    """
    return os.path.relpath(
        project_root,
        os.path.realpath(output_dir),
    )


def abs_from_root(root: str, rel: str) -> str:
    return os.path.normpath(os.path.join(os.path.dirname(root), rel))
