# -*- coding: utf-8 -*-
r"""
Module contains functions:
- load eigenvector by number and state
- load specific eigenvector by its filename
"""
from pathlib import Path
from typing import List, TypeVar
import numpy as np

PathLike = TypeVar("PathLike", str, Path)


def load_vector_by_number(path: PathLike, state: str = 'sp', number: int = 1) -> List[np.ndarray]:
    r"""
    loads a specific eigenvector

    Args:
        path(Path): path of directory for the eigenvector
        state(str): String decider whether initial state (ini), saddlepoint state (sp) or final state (fin) should
        be addressed.
        number(int): number of the eigenvector. Default is the first eigenvector

    Returns:
        A list of numpy arrays: x,y,z,vecx,vecy,vecz representing the eigenvector
    """
    if number >= 10:
        filename = 'vector_' + state + '.dat_00' + str(number) + '.dat'
    else:
        filename = 'vector_' + state + '.dat_000' + str(number) + '.dat'
    file = open(path / filename, 'r')
    x, y, z = [], [], []
    vec_x, vec_y, vec_z, v = [], [], [], []
    for line in file:
        L = line.split()
        x.append(float(L[0]))
        y.append(float(L[1]))
        z.append(float(L[2]))
        vec_x.append(float(L[3]))
        vec_y.append(float(L[4]))
        vec_z.append(float(L[5]))
        v.append(float(L[6]))
    return [np.array(x), np.array(y), np.array(z), np.array(vec_x), np.array(vec_y), np.array(vec_z), np.array(v)]


def load_vector_by_name(path: PathLike) -> List[np.ndarray]:
    r"""
    loads a specific eigenvector

    Args:
        path(Path): path ot the specific eigenvector

    Returns:
        A list of numpy arrays: x,y,z,vecx,vecy,vecz, v representing the eigenvector
    """
    file = open(path, 'r')
    x, y, z = [], [], []
    vec_x, vec_y, vec_z, v = [], [], [], []
    for line in file:
        L = line.split()
        x.append(float(L[0]))
        y.append(float(L[1]))
        z.append(float(L[2]))
        vec_x.append(float(L[3]))
        vec_y.append(float(L[4]))
        vec_z.append(float(L[5]))
        v.append(float(L[6]))
    return [np.array(x), np.array(y), np.array(z), np.array(vec_x), np.array(vec_y), np.array(vec_z), np.array(v)]
