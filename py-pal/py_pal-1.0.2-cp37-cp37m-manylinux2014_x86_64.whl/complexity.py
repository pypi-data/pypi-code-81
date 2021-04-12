"""Definition of complexity classes."""

import numpy as np
from numpy import ma


class NotFittedError(Exception):
    pass


class UnderDeterminedEquation(Exception):
    pass


class Complexity:
    """ Abstract class that fits complexity classes to timing data."""

    def __init__(self):
        # list of parameters of the fitted function class as returned by the
        # last square method np.linalg.lstsq
        self.coeff = None

    def fit(self, n, t):
        """ Fit complexity class parameters to timing data.

        Input:
        ------

        n -- Array of values of N for which execution time has been measured.

        t -- Array of execution times for each N in seconds.

        Output:
        -------

        residuals -- Sum of square errors of fit
        """
        x = self._transform_n(n)
        y = self._transform_y(t)

        coeff, residuals, rank, s = np.linalg.lstsq(x, y, rcond=-1)

        if len(residuals) == 0:
            raise UnderDeterminedEquation

        self.coeff = coeff
        return residuals[0]

    def compute(self, n):
        """ Compute the value of the fitted function at `n`. """
        if self.coeff is None:
            raise NotFittedError()

        # Result is linear combination of the terms with the fitted coefficients
        x = self._transform_n(n)
        tot = 0
        for i in range(len(self.coeff)):
            tot += self.coeff[i] * x[:, i]
        return tot

    def __str__(self):
        prefix = '{}: '.format(self.__class__.__name__)

        if self.coeff is None:
            return prefix + ': not yet fitted'
        return prefix + self.format_str().format(*tuple(self.coeff))

    # --- abstract methods

    @classmethod
    def format_str(cls):
        """ Return a string describing the fitted function.

        The string must contain one formatting argument for each coefficient.
        """
        return 'FORMAT STRING NOT DEFINED'

    def _transform_n(self, n):
        """ Terms of the linear combination defining the complexity class.

        Output format: number of Ns x number of coefficients .
        """
        raise NotImplementedError()

    def _transform_y(self, t):
        """ Transform time as needed for fitting.
        (e.g., t->log(t)) for exponential class.
        """
        return t

    def __gt__(self, other):
        if self.__class__ == other.__class__ and self.coeff is not None and other.coeff is not None:
            return self.coeff[-1] > other.coeff[-1]
        return ALL_CLASSES.index(self.__class__) > ALL_CLASSES.index(other.__class__)


# --- Concrete implementations of the most popular complexity classes

class Constant(Complexity):
    def _transform_n(self, n):
        return np.ones((len(n), 1))

    @classmethod
    def format_str(cls):
        return '= {:.2G}'


class Linear(Complexity):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n]).T

    @classmethod
    def format_str(cls):
        return '= {:.2G} + {:.2G}*n'


class Quadratic(Complexity):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n * n]).T

    @classmethod
    def format_str(cls):
        return '= {:.2G} + {:.2G}*n^2'


class Cubic(Complexity):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n ** 3]).T

    @classmethod
    def format_str(cls):
        return '= {:.2G} + {:.2G}*n^3'


class Logarithmic(Complexity):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), np.log(n)]).T

    @classmethod
    def format_str(cls):
        return '= {:.2G} + {:.2G}*log(n)'


class Linearithmic(Complexity):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n * np.log(n)]).T

    @classmethod
    def format_str(cls):
        return '= {:.2G} + {:.2G}*n*log(n)'


class Polynomial(Complexity):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), np.log(n)]).T

    def _transform_y(self, t):
        masked = ma.log(t)
        return masked.filled(0)

    @classmethod
    def format_str(cls):
        return '= {:.2G} * x^{:.2G}'


class Exponential(Complexity):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n]).T

    def _transform_y(self, t):
        masked = ma.log(t)
        return masked.filled(0)

    @classmethod
    def format_str(cls):
        return '= {:.2G} * {:.2G}^n'


ALL_CLASSES = [Constant, Logarithmic, Linear, Linearithmic, Quadratic, Cubic, Polynomial, Exponential]
