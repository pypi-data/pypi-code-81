# -*- coding: utf-8 -*-
r"""
Analyzing the results for the two spin precision tests
"""
from tests.ianalyze import IAnalyzer
from scipy.optimize import curve_fit
import numpy as np
from typing import Callable, Tuple
from pathlib import Path
from python3.shell_commands import writelog


class CAnalyzePrecisionWithoutDamping(IAnalyzer):
    r"""
    Class responsible for analyzing the results of the two spin precision tests
    """

    def __init__(self, logfile: Path, J: float, tempdir: Path, lowerline: int, upperline: int,
                 acceptance_level: float = 1e-2) -> None:
        r"""
        Initializes the analyzer

        Args:
            logfile(Path): log file

            J(float): strength of the interlayer exchange. The type of the interlayer exchange does not affect the
            results of the test.

            tempdir(Path): temporary directory for the calculation

            lowerline(int), upperline(int): index of the line in the STM-file in which the lower spin and the upper spin
            is placed.

            acceptance_level(float): Discrepancy between analytic result and precision frequency determined by fit which
            is allowed to pass the test.
        """
        self._J = J
        self.logfile = logfile
        self.tempdir = tempdir
        self.accept = acceptance_level
        self.lowerline = lowerline
        self.upperline = upperline

    def read_spinevolution(self) -> Tuple[np.ndarray, np.ndarray]:
        r"""
        Reads the time evolution of the upper and the lower spin.

        Returns:
            lower spin and upper spin over time: lowerspin=[[sxt0,syt0,szt0],...]
        """
        lowerspin, upperspin = [], []
        for i in range(100):
            file = open(str(self.tempdir / ('SpinSTM_' + str(i) + '.dat')), 'r')
            ll = 0
            for line in file:
                L = line.split()
                if ll == self.lowerline:
                    lowerspin.append([float(L[3]), float(L[4]), float(L[5])])
                elif ll == self.upperline:
                    upperspin.append([float(L[3]), float(L[4]), float(L[5])])
                else:
                    pass
                ll += 1
        return np.asarray(lowerspin), np.asarray(upperspin)

    def __call__(self) -> bool:
        r"""
        Start analyzing

        Returns:
            all(subtest_results)
        """
        lowerspin, upperspin = self.read_spinevolution()
        # time in ps
        time = np.arange(start=0, stop=100, step=1) * 0.01
        # fit model to upper spin
        subtests = []
        components = ['x', 'y', 'z']
        writelog(self.logfile, message='Checking upper spin precision frequency:...')
        for (idx, c) in enumerate(components):
            writelog(self.logfile, message='      ' + c + '-component:...', end='')
            popt, pcov = curve_fit(self.s_upper(component=c), time, upperspin[:, idx], p0=[self.analytic_frequency()])
            writelog(self.logfile, f'Expected: {self.analytic_frequency()}, Result from Fit: {popt[0]}')
            if abs(popt[0]-self.analytic_frequency()) <= self.accept:
                subtests.append(True)
                writelog(self.logfile, f'      Difference: {abs(popt[0]-self.analytic_frequency())} <'
                                       f' {self.accept}...Passed')
            else:
                subtests.append(False)
                writelog(self.logfile, f'      Difference: {abs(popt[0] - self.analytic_frequency())} >'
                                       f' {self.accept}...Failed!')

        return all(subtests)

        """plt.plot(time, upperspin[:, 0], 'k+')
        plt.plot(time, self.s_upper('x')(t=time, frequency=poptx[0]))
        plt.plot(time, upperspin[:, 1], 'k+')
        plt.plot(time, self.s_upper('y')(t=time, frequency=popty[0]))
        plt.plot(time, upperspin[:, 2], 'k+')
        plt.plot(time, self.s_upper('z')(t=time, frequency=poptz[0]))
        plt.show()"""

    def s_upper(self, component: str) -> Callable:
        r"""
        model functions for upper spin

        Args:
            component(str): say which component of spin is adressed (x, y, z)

        Returns:
            fit function
        """

        def sx(t: np.ndarray, frequency: float) -> np.ndarray:
            r"""
            model function for x component of upper spin

            Args:
                t(np.ndarray): time
                frequency(float): precision frequency

            Returns:
                time evolution of spin component
            """
            return 0.5 * np.cos(t * frequency) + 0.5

        def sy(t: np.ndarray, frequency: float) -> np.ndarray:
            r"""
            model function for y component of upper spin (see sx)
            """
            return (np.sqrt(8) / 4) * np.sin(frequency * t)

        def sz(t: np.ndarray, frequency: float) -> np.ndarray:
            r"""
            model function for z component of upper spin (see sx)
            """
            return -0.5 * np.cos(frequency * t) + 0.5

        if component == 'x':
            return sx
        elif component == 'y':
            return sy
        elif component == 'z':
            return sz

    def analytic_frequency(self) -> float:
        r"""
        Returns:
            the analytic precision frequency. This depends only on the interlayer exchange.
        """
        # constants:
        g = 2.002319304
        hbar = 6.582119569 * 10 ** (-4)  # in eVps
        J = self._J / 1000  # in eV
        return (np.sqrt(8) * g * J) / hbar


