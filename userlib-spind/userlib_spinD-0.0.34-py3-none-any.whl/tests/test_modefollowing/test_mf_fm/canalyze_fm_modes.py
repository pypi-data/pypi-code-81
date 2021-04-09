# -*- coding: utf-8 -*-
r"""
Analyzes the results of the modefollowing testing procedure for the ferromagnetic magnon modes.
"""
from tests.ianalyze import IAnalyzer
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Tuple
import matplotlib.pyplot as plt
import scipy.optimize


class CAnalyzeFmModes(IAnalyzer):
    r"""
    Class which compares the dispersion of the magnon mode (calculated with MF-method) with the corresponding eigen-
    value of the Hessian.
    """

    def __init__(self, logfile: Path, tempdir: Path, modenr: int, acceptance_level: float = 1e-2) -> None:
        r"""
        Initializes the analyzer for the mode following test for the magnon modes.

        Args:
            logfile(Path): logfile for the results of the tests
            tempdir(Path): temporary directory for the test calculation
            modenr(int): Number of the calculated mode
            acceptance_level(float): acceptance level. Difference between fitting the eigenmode determined by MF and
            corresponding eigenvalue of the hessian which is accepted.
        """
        self.modenr = modenr
        self.logfile = logfile
        self.tempdir = tempdir

    def __call__(self) -> bool:
        r"""
        Calls the analyzing
        """
        l_ev = self._geteigenvalue()
        l_steps_integrated, l_energy = self._getdatamodefollowing()
        popt, pcov = scipy.optimize.curve_fit(self.parabola, l_steps_integrated, l_energy, p0=[l_ev])
        l_ev_fit = popt[0]
        print(abs(l_ev_fit-l_ev))
        plt.plot(l_steps_integrated, self.parabola(l_steps_integrated, l_ev_fit), 'r-')
        plt.plot(l_steps_integrated, l_energy, 'k+')

        plt.show()

        return True

    def _geteigenvalue(self) -> float:
        r"""
        Reads the corresponding eigenvalue from the first calculation of the hessian. This value will be compared to the
        result of the fit.
        """
        with open(str(self.tempdir / 'vtp_eig.dat'), 'r') as f:
            for line in f:
                # only read the first line. This line corresponds to the hessian of the untranslated spin configuration
                L = line.split()
                l_ev = float(L[self.modenr])
                break
        return l_ev

    def _getdatamodefollowing(self) -> Tuple[np.ndarray, np.ndarray]:
        r"""
        Read the information from the negative and positive direction, concat them and integrate the steps. An arbitrary
        negative sign is assigned to the negative direction.

        Returns:
            the integrated elongation along the mode (called q_p in Stephans Thesis) and the energy as np arrays.
        """
        # read positive direction:
        dfp = pd.read_csv(self.tempdir / 'vtp_energy.dat', sep=r'\s+', usecols=[0, 1, 2],
                          names=['step', 'energy', 'ds'],
                          index_col=False)
        dfp['ds_integrated'] = pd.Series(np.cumsum(dfp['ds'].to_numpy()))
        # energy zero point
        e0 = dfp['energy'].to_numpy()[0]

        # read negative direction assign negative sign:
        dfn = pd.read_csv(self.tempdir / 'vtn_energy.dat', sep=r'\s+', usecols=[0, 1, 2],
                          names=['step', 'energy', 'ds'],
                          index_col=False)
        dfn['ds_integrated'] = pd.Series(np.cumsum(dfn['ds'].to_numpy() * -1))

        l_df_tot = pd.concat([dfn, dfp])
        l_df_tot['energy'] = l_df_tot['energy'] - e0
        l_df_tot.sort_values(by=['ds_integrated'], ascending=True, inplace=True)


        dfn.to_csv('dfntest.txt', index=False)
        dfp.to_csv('dfptest.txt', index=False)
        l_df_tot.to_csv('dftottest.txt', index=False)

        return l_df_tot['ds_integrated'].to_numpy(), l_df_tot['energy'].to_numpy()

    @staticmethod
    def parabola(q_p: np.ndarray, ev) -> np.ndarray:
        r"""
        Model function for fitting the magnon dispersion which is quadratic. Make sure the data is shifted such that the
        minimum of the parabola is centered at 0,0.

        Args:
            q_p(np.ndarray): elongation along the mode
            ev(float): curvature of the parabola. Representing the eigenvalue.

        Returns:
            Dispersion (energy) as numpy array
        """
        return 0.5 * ev * q_p ** 2
