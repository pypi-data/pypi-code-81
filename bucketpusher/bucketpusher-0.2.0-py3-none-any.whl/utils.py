import datetime
import shutil
import platform
import subprocess
import glob
import pathlib


def _find_parent(path):
    """
    This is to extract the parent directory of a wildcard without causing
    syntax issues on Windows
    """
    parent = pathlib.Path("")
    for part in path.parts:
        tmp = parent / part
        try:
            if not tmp.exists():
                break
        except Exception:
            break
        parent = tmp
        if parent == path:
            parent = path.parent
            break
    return parent


def parse_paths(paths, recursive=True):
    """
    Iterates over all file paths found in `paths`. The iterator yields a tuple
    of two elements, described as follows.

    For a given file, the first element of the tuple is the file path and the
    second is the file path relative to the parent of the specified path.

    For example,
    parse_paths('parent/dir-with-sub-dirs', True) might yield the following tuples

    (pathlib.Path('parent/dir-with-sub-dirs/f1.txt'),
     pathlib.Path('dir-with-sub-dirs/f1.txt'))

    and

    (pathlib.Path('parent/dir-with-sub-dirs/sub-dir/f2.txt'),
    pathlib.Path('dir-with-sub-dirs/sub-dir/f1.txt'))

    and `parse_paths('dir-with-sub-idirs/f1.txt')` would yield
    (pathlib.Path('dir-with-sub-dirs/f1.txt'), pathlib.Path('f1.txt'))
    """
    if isinstance(paths, str):
        paths = [paths]
    for p in paths:
        path = pathlib.Path(p).expanduser()
        path_str = str(path)
        parent = path.parent
        if path.is_dir():
            path_str = f"{path}/**"
        for _ in glob.iglob(path_str, recursive=recursive):
            path2 = pathlib.Path(_)
            if path2.is_file():
                yield (path2, path2.relative_to(parent))


def open(filepath):
    check = True
    app = None
    if platform.system() == "Windows":
        app = "explorer.exe"
        # explorer returns non-zero regardless..
        check = False
    elif platform.system() == "Darwin":
        app = "open"
    elif platform.system() == "Linux":
        app = "xdg-open"

    if app is None or not shutil.which(app):
        raise OSError(f"No known default application for opening {filepath}")
    if not filepath.is_file():
        raise ValueError(f"{filepath} does not exist")
    try:
        subprocess.run([app, str(filepath)], check=check)
    except subprocess.CalledProcessError:
        raise OSError(f"Error trying to open {filepath}")
    except OSError:
        raise OSError("No known default application")


def display_bytes(size):
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size >= 1024 and i < (len(units) - 1):
        size = size / 1024
        i += 1
    return f"{size:.2f} {units[i]}"


def display_time(seconds):
    return datetime.timedelta(seconds=int(seconds))


def path_or_partial_path_exists(path):
    path = pathlib.Path(path)
    try:
        if path.exists():
            return True
    except Exception:
        pass

    parent = pathlib.Path("")
    for part in path.parts:
        tmp = parent / part
        try:
            if tmp.exists():
                return True
        except Exception:
            pass
        parent = tmp
    return False
