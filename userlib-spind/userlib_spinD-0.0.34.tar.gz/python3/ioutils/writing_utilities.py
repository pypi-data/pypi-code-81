# -*- coding: utf-8 -*-
r"""
module with functions:
- write eigenvector
"""
from pathlib import Path
from typing import List, TypeVar
import numpy as np

PathLike = TypeVar("PathLike", str, Path)


def write_vector(vec: List[np.ndarray], outfile: PathLike) -> None:
    r"""
    Writes eigenvector to file

    Args:
        vec(List[np.ndarray]): eigenvector in format [x, y, z, vx, vy, vz, |v|]
        outfile(PathLike): name of the created out file
    """
    wfile = open(outfile, 'a')
    for (idx, line) in enumerate(vec[0]):
        wfile.write(str(vec[0][idx]) + ' ' + str(vec[1][idx]) + ' ' + str(vec[2][idx]) + ' ' + str(vec[3][idx]) +
                    ' ' + str(vec[4][idx]) + ' ' + str(vec[5][idx]) + ' ' + str(vec[6][idx]) + '\n')
    wfile.close()
