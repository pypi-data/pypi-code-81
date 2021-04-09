# -*- coding: utf-8 -*-
r"""
Module for classes analyzing the differences between properties of the magnetizations of the different layers of a
multilayer system.
"""
from pathlib import Path
from typing import TypeVar, Union
import pandas as pd
import numpy as np
import os

PathLike = TypeVar("PathLike", str, Path)


class CMagDiffCubicLayers:
    r"""
    this class is responsible for calculating the differences between two cubic stacked layers. This can be used to
    measure how simultaneous a collapse might be.
    """

    def __init__(self, allspinfiles: bool = True, spinfileslocation: Path = Path.cwd(),
                 specificfile: PathLike = 'spin_0001.dat', method: str = 'vincenty') -> None:
        r"""
        initializes the calculation of the magnetization deviations in both layers.

        Args:
            allspinfiles(bool): Flag whether all spin_xxx.dat files shell be read and analyzed. The default is True. In this
            case the input parameter vtfileslocation determines where the files should be.

            spinfileslocation(PathLike): All the spin files. Default path is current working directory

            specificfile(PathLike): Only necessary if allspinfiles is False. Then a specific spin-file is analyzed. The
            default is spin_0001.dat here.

            method(str): formula to calculate the difference. Either spherical law of cosines (cosine), haversines
            formula (haversine), vincentys formula (vincenty) or simple difference of the vectors (diff)
        """
        self._allspinfiles = allspinfiles
        self._spinfileslocation = spinfileslocation
        self._specificfile = specificfile
        self._method = method

    def __call__(self) -> Union[float, np.ndarray]:
        r"""
        Calls the calculation

        Returns:
            either a float representing the difference of a configuration of a specific file or a 2d numpy array with
            the following structure [[step1, diff1],[step2,diff2],...]
        """
        if self._allspinfiles:
            l_diff, stepindices = [], []
            l_files = self._spinfileslocation.glob('*.*')
            for f in l_files:
                if str(f.name).startswith('spin_'):
                    stepindices.append(int(str(f.name)[5:-4]))
                    df = pd.read_csv(f, sep=r"\s+", index_col=False, usecols=[0, 1, 2, 3, 4, 5],
                                     names=['x', 'y', 'z', 'sx', 'sy', 'sz'])
                    l_df_lower = df.loc[df['z'] == 0.0]
                    l_df_upper = df.loc[df['z'] != 0.0]
                    l_diff.append(self.calculatedifference(dfup=l_df_upper, dfdown=l_df_lower))
            l_diff = np.asarray(l_diff)
            l_steps = np.asarray(stepindices)
            return np.column_stack((l_steps, l_diff))
        else:
            df = pd.read_csv(self._specificfile, sep=r"\s+", index_col=False, usecols=[0, 1, 2, 3, 4, 5],
                             names=['x', 'y', 'z', 'sx', 'sy', 'sz'])
            l_df_lower = df['z'] == 0.0
            l_df_upper = df['z'] != 0.0
            return self.calculatedifference(dfup=l_df_upper, dfdown=l_df_lower)

    def calculatedifference(self, dfup: pd.DataFrame, dfdown: pd.DataFrame) -> float:
        r"""
        Applies the chosen method to calculate the difference between the magnetizations of two equal lattices or
        representations of the same lattice respectively.

        Args:
            dfup(DataFrame): data frame for the upper layer
            dfdown(DataFrame): data frame for the lower layer

        Returns:
            float representing the difference
        """
        if self._method == 'diff':
            return self.vectordifference(dfup, dfdown)
        elif self._method == 'cosine':
            raise NotImplementedError('Spherical cosine is not implemented yet')
        elif self._method == 'haversine':
            raise NotImplementedError('Haversine formula is not implemented yet')
        elif self._method == 'vincenty':
            return self.vincentydifference(dfup, dfdown)
        else:
            raise ValueError('This is not a valid method to calculate the difference')

    @staticmethod
    def arctan2(y: float, x: float) -> Union[float, None]:
        r"""
        Calculates arctan2 following Pavels GNEB paper
        """
        if x > 0:
            return np.arctan(y / x)
        elif x < 0:
            if y >= 0:
                return np.arctan(y / x) + np.pi
            elif y < 0:
                return np.arctan(y / x) - np.pi
        elif x == 0:
            if y > 0:
                return np.pi / 2
            elif y < 0:
                return -1 * np.pi / 2
            if y == 0:
                print('Warning arctan2: x and y are zero')
                return None

    def vincentydifference(self, dfup: pd.DataFrame, dfdown: pd.DataFrame) -> float:
        r"""
        Difference according to vincentys formula as described in Pavels GNEB paper

        Args:
            dfup(DataFrame): data frame for the upper layer
            dfdown(DataFrame): data frame for the lower layer

        Returns:
            float representing the difference
        """
        sx_u = dfup['sx'].to_numpy()
        sy_u = dfup['sy'].to_numpy()
        sz_u = dfup['sz'].to_numpy()
        sx_d = dfdown['sx'].to_numpy()
        sy_d = dfdown['sy'].to_numpy()
        sz_d = dfdown['sz'].to_numpy()
        # restructure data
        mag_u = np.asarray([sx_u, sy_u, sz_u]).T
        mag_d = np.asarray([sx_d, sy_d, sz_d]).T
        d = []
        for (idx, mu) in enumerate(mag_u):
            md = mag_d[idx]
            y = np.linalg.norm(np.cross(mu, md))
            x = mu[0]*md[0] + mu[1]*md[1] + mu[2]*md[2]
            d.append(np.arctan2(y, x))
        return np.linalg.norm(np.array(d))

    @staticmethod
    def vectordifference(dfup: pd.DataFrame, dfdown: pd.DataFrame) -> float:
        r"""
        Simple difference between the vectors of the lower and upper layer

        Args:
            dfup(DataFrame): data frame for the upper layer
            dfdown(DataFrame): data frame for the lower layer

        Returns:
            float representing the difference
        """
        diffx = dfdown['sx'].to_numpy() - dfup['sx'].to_numpy()
        diffy = dfdown['sy'].to_numpy() - dfup['sy'].to_numpy()
        diffz = dfdown['sz'].to_numpy() - dfup['sz'].to_numpy()
        vec_diff = np.column_stack((diffx, diffy, diffz))
        return np.sum(np.linalg.norm(vec_diff, axis=1))[0]
