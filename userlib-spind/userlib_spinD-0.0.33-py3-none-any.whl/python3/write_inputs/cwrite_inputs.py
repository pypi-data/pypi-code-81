# -*- coding: utf-8 -*-
r"""
This module takes care of writing input files for calculations with the SpinD-code
"""
from typing import TypeVar, List
from pathlib import Path
from python3.shell_commands import adjust_parameter

PathLike = TypeVar("PathLike", str, Path)


class CWriteInput:
    r"""
    General class for writing input files
    """

    def __init__(self, file: PathLike, **kwargs) -> None:
        r"""
        Initializes writing of input file

        Args:
            name(PathLike): name of the created file or path to the file that shall be created.
        """
        self.file = file
        self.content = dict(**kwargs)

    def __call__(self) -> None:
        r"""
        Calls the writing
        """
        for (key, value) in self.content.items():
            with open(self.file, 'a') as f:
                f.write(key + ' ' + value + '\n')

    def appendline(self, key: str, value: str) -> None:
        r"""
        Appends a line to the input file
        """
        with open(self.file, 'a') as f:
            f.write(key + ' ' + value + '\n')

    def appendmultilinevalues(self, key: str, values: List[str]) -> None:
        r"""
        Some input files have multiple lines of values after a key line. E. g. lattice in lattice in. In this case
        provide the key line as key and each following line in a list of strings
        """
        with open(self.file, 'a') as f:
            f.write(key + '\n')
            for line in values:
                f.write(line + '\n')

    def replaceline(self, key: str, value: str) -> None:
        r"""
        Replaces the line addressed by key with key + value
        """
        adjust_parameter(keyword=key, value=value, directory_file=self.file)
