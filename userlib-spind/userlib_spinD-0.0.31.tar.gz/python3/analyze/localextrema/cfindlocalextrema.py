# -*- coding: utf-8 -*-
r"""
module for finding local extrema in data. Useful for example in:

- vector translation / mode following: The vector translation produces an outputfile vt_energy.dat. Sometimes one is
interested in investigating the local minima and maxima of the behaviour along the mode in more detail. Therefore one
wants to know the step at which the extremum occurs.
"""
from pathlib import Path
from typing import List, TypeVar, Union, Tuple
import numpy as np
import pandas as pd
from scipy.signal import argrelextrema

PathLike = TypeVar("PathLike", str, Path)


class CFindLocalExtremaModeFollowing:
    r"""
    Class for finding local extrema in vt_energy.dat
    """
    def __init__(self, data: pd.DataFrame = None, filename: PathLike = 'vt_energy.dat') -> None:
        r"""
        Initializes the localization of local minima and maxima within vt_energy.dat

        Args:
            data(DataFrame): data frame containing columns steps and energy. If None the file vt_energy.in is tried to
            read. Another filename can be provided also.
        """
        if data is None:
            self._df = pd.read_csv(filename, usecols=[0, 1], sep=r"\s+", names=['step', 'energy'], index_col=False)
        else:
            self._df = data

        self._energy = self._df['energy'].to_numpy()
        self._step = self._df['step'].to_numpy()

    def __call__(self, method: str = 'scipy', writeoutfile: bool = False) -> Tuple[np.ndarray, np.ndarray]:
        r"""
        Calls analyzing the energy whether local minima exists.

        Args:
            method(str): method for finding the relative extrema. Default is the use of scipys argrelextrema.
            writeoutfile(bool): Whether results shall be written to file.

        Returns:
            array of indices of local maxima and array of indices of local minima
        """
        if method == 'scipy':
            maxs = argrelextrema(self._energy, np.greater)[0]
            mins = argrelextrema(self._energy, np.less)[0]
            if writeoutfile:
                with open('vt_extrema.dat', 'w') as f:
                    f.write('step energy type \n')
                    for mx in maxs:
                        f.write(f'{self._step[mx]} {self._energy[mx]} max \n')
                    for mn in mins:
                        f.write(f'{self._step[mn]} {self._energy[mn]} min \n')
            return maxs, mins
        else:
            raise NotImplementedError('other methods not yet available!')
