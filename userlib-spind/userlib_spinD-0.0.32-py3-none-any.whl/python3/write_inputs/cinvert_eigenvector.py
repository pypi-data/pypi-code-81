# -*- coding: utf-8 -*-
r"""
This module contains the class that takes care of inverting an eigenvector. This is useful in modefollowing approaches
where one wants to investigate both branches of the parabola.
"""
from python3.ioutils.loading_utilities import load_vector_by_name
from python3.ioutils.writing_utilities import write_vector
from typing import TypeVar, List
from pathlib import Path

PathLike = TypeVar("PathLike", str, Path)
import numpy as np


class CInvertEigenvector:
    r"""
    Class for inverting an eigenvector. By means of the htst one can multiply an eigenvector with -1 and get the
    inverted one
    """

    def __init__(self, vector_original: PathLike) -> None:
        r"""
        Initializes the inverting of an eigenvector

        Args:
            vector_original (PathLike): Original eigenvector which shall be inverted.
        """
        self._ev_original = load_vector_by_name(vector_original)

    def __call__(self, outfile: PathLike) -> None:
        r"""
        calls the inverting. Writes out to file:

        Args:
            outfile(PathLike): file to which the inverted eigenvector is written
        """
        write_vector(self._invert_vector(self._ev_original), outfile=outfile)

    @classmethod
    def _invert_vector(cls, vec: List[np.ndarray]) -> List[np.ndarray]:
        r"""
        inverts eigenvector

        Args:
            vec(List[np.ndarray]): eigenvector in format [x, y, z, vx, vy, vz, |v|]

        Returns:
            inverted eigenvector: [x, y, z, -vx, -vy, -vz, |v|]
        """
        return [vec[0], vec[1], vec[2], -1 * vec[3], -1 * vec[4], -1 * vec[5], vec[6]]
