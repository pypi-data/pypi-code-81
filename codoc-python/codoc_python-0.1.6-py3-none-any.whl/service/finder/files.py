#!/usr/bin/env python3
from typing import Set
from pathlib import Path


def get_all_python_files(path: str = None) -> Set[Path]:
    return {f for f in get_all_files(path) if f.suffix == ".py"}


def get_all_files(path: str = None) -> Set[Path]:
    if path is None:
        path = Path.cwd()
    folders = {Path(path)}
    files = set()
    while folders:
        folder = folders.pop()
        try:
            children = {f for f in Path(folder).iterdir()}
        except FileNotFoundError:
            raise CodocFolderNotFound(path)

        folders |= {f for f in children if f.is_dir()}
        files |= {f for f in children if f.is_file()}
    return files


class CodocFolderNotFound(Exception):
    def __init__(self, path):
        super().__init__(f"codoc_views folder '{path}' not found in current directory")
