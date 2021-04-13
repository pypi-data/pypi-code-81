"""
Module where you can configure and process paths.
"""
from pathlib import Path
import sys
import mylogging


# Root is usually current working directory, if not, use `set_paths` function.
root_path = None
app_path = None
init_path = None


def set_paths(set_root_path=None, set_init_path=None):
    """Parse python project application structure, add paths to sys.path and save to mypythontools config
    for other functions to use.

    Args:
        set_root_path ((str, pathlib.Path)): Path to project root where tests and docs folder are.
            If None, then cwd (current working directory) is used. Defaults to None.
        set_init_path ((str, pathlib.Path)): Path to project `__init__.py`. If None, then first
            found `__init__.py` is used. Defaults to None.
    """
    global init_path
    global app_path

    set_root(set_root_path=set_root_path)

    init_path = (
        find_path("__init__.py", root_path)
        if not set_init_path
        else Path(set_init_path)
    )
    app_path = init_path.parent


def set_root(set_root_path=None):
    """Set project root path and add it to sys.path if it's not already there.

    Args:
        set_root_path ((str, pathlib.Path)): Path to project root where tests and docs folder are.
            If None, then cwd (current working directory) is used. Defaults to None.
    """
    global root_path

    root_path = Path(set_root_path) if set_root_path else Path.cwd()

    if not root_path.as_posix() in sys.path:
        sys.path.insert(0, root_path.as_posix())


def find_path(file, folder=None, exclude=["node_modules", "build", "dist"], levels=5):
    """Look on files in folder (cwd() by default) and find file with it's folder.

    Args:
        file (str): Name with extension e.g. "app.py".
        folder (str): Where to search. If None, then root_path is used (cwd by default). Defaults to None.
        exclude (str): List of folder names (anywhere in path) that will be ignored. Defaults to ['node_modules', 'build', 'dist'].
        levels (str): Recursive number of analyzed folders. Defaults to 3.

    Returns:
        Path: Path of file.

    Raises:
        FileNotFoundError: If file is not found.
    """

    folder = root_path if not folder else Path(folder).resolve()

    for lev in range(levels):
        glob_file_str = f"{'*/' * lev}{file}"

        for i in folder.glob(glob_file_str):
            isthatfile = True
            for j in exclude:
                if j in i.parts:
                    isthatfile = False
                    break
            if isthatfile:
                return i

    # If not returned - not found
    raise FileNotFoundError(mylogging.return_str(f"File `{file}` not found"))
