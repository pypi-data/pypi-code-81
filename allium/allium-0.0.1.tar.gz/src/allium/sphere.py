from functools import wraps

import numpy as np

from scipy.optimize import brentq
from scipy.special import spherical_jn as j
from scipy.special import spherical_yn as y

def check_lengths(func):
    """Decorator to check that ``c`` and ``R`` are of the same length
    before performing calculations that might otherwise quietly produce
    nonsensical results."""

    @wraps(func)
    def checked_func(obj, *args, **kwargs):
        assert len(obj.c) == len(obj.R), \
            "c and R have different lengths %i and %i" % (len(obj.c), len(obj.R))
        return func(obj, *args, **kwargs)

    return checked_func


class Sphere(object):
    """A class for computing eigenfrequencies and eigenfunctions of a
    sphere with a (radially) piecewise-constant sound-speed profile.
    The class is initialised with arrays for the sound speeds ``c``
    and outer radii ``R`` of each shell, which should be of equal
    length.  The attributes
    ``c`` and ``R`` can also be directly modified after the object is
    initialised.

    The thickness of each shell can be accessed by the property ``dR``
    and the asymptotic large separation by ``Delta_omega``.

    The default initialisation corresponds to a sphere with radius 1
    and constant sound speed 1.

    All frequencies are *angular* frequencies.

    Parameters
    ----------
    c: iterable of floats
        Sound speeds of each shell (default=``[1.0]``)
    R: iterable of floats
        Radii of outer edge of each shell (default=``[1.0]``).

    """
    def __init__(self, c=[1.0], R=[1.0]):
        self.c = c
        self.R = R
        self.eigenfrequencies = {}


    def __getitem__(self, key):
        if isinstance(key, tuple) and len(key) == 2:
            return self.eigenfrequencies[key[0]][key[1]]
        else:
            return self.eigenfrequencies[key]


    @property
    def dR(self):
        """Thickness of each radial shell."""
        return np.hstack([self.R[0], np.diff(self.R)])


    @property
    def Delta_omega(self):
        """The asymptotic large separation
        :math:`\\Delta\\omega=\\pi/\\int_0^R(dr/c)`."""
        return np.pi/np.sum(self.dR/np.array(self.c))


    def search_eigenfrequencies(self, l, f):
        """Search for an eigenfrequency of angular degree(s) ``l`` between
        each consecutive pair of frequencies in the array ``f``.
        Output is added to the
        dict ``self.eigenfrequencies``, whose keys are the angular
        degrees searched (i.e. ``l``) and items are lists of
        eigenfrequencies.  Re-running for the same angular degree will
        replace (not extend) the results in ``self.eigenfrequencies``.

        Because ``eigenfrequencies`` is a long word to type, the
        ``Sphere`` object itself can be indexed to get the
        eigenfrequencies, including by using tuples and slices,
        e.g. ``self[0,5:10]`` returns
        ``self.eigenfrequencies[0][5:10]``.

        Parameters
        ----------
        l: int or list of ints
            The angular degree(s) for which to search for modes.
        f: iterable of floats
            The frequency range in which to search for mode.  One root
            find is performed for each pair of values in
            ``f``. i.e. between ``f[0]`` and ``f[1]``, ``f[1]`` and
            ``f[2]``, etc. up to ``f[len(f)-2]`` and ``f[len(f)-1]``.

        """
        if isinstance(l, (int, np.integer)):
            l = [l]

        for li in l:
            self.eigenfrequencies[li] = []
            for i in range(1, len(f)):
                try:
                    self.eigenfrequencies[li].append(brentq(lambda w: self.residual(li, w), f[i-1], f[i]))
                except ValueError:
                    continue

    @check_lengths
    def wavefunction(self, l, omega):
        """Given angular degree ``l`` and frequency ``omega``, returns the
        wavefunction as a function that can then be evaluated at the
        desired radii ``r``.  Note that this is not necessarily an
        eigenfunction, unless ``omega`` is a mode frequency.
        """
        if len(self.c) == 1:
            def f(r):
                return j(l, omega*r/self.c[0])
        else:
            x = self.solve_coefficients(l, omega)
            def f(r):
                z = np.zeros_like(r)
                I = (r <= self.R[0])
                z[I] = j(l, omega*r[I]/self.c[0])
                for i in range(1,len(self.c)):
                    I = (self.R[i-1] < r) & (r <= self.R[i])
                    kr = omega*r[I]/self.c[i]
                    z[I] = x[(i-1)*2]*j(l, kr) + x[(i-1)*2+1]*y(l, kr)

                return z

        return f


    def eigenfunction(self, l, i):
        """Returns the eigenfunction of the ``i``-th frequency of angular
        degree ``l``, according to the results of the frequency
        search, as a function that can then be evaluated at the
        desired radius ``r``.  Really just evaluates :py:meth:`wavefunction`
        at frequency ``self.eigenfrequencies[l][i]``."""
        return self.wavefunction(l, self.eigenfrequencies[l][i])
    

    @check_lengths
    def residual(self, l, omega):
        """Given angular degree ``l`` and frequency ``omega``, returns the
        value of the wavefunction at the outer boundary, which the
        solver uses as a residual to find eigenfrequencies."""
        if len(self.c) == 1:
            return(j(l, omega*self.R[0]/self.c[0]))
        else:
            x = self.solve_coefficients(l, omega)
            return x[-2]*j(l, omega*self.R[-1]/self.c[-1]) + x[-1]*y(l, omega*self.R[-1]/self.c[-1])
    

    @check_lengths
    def solve_coefficients(self, l, omega):
        """Given angular degree ``l`` and frequency ``omega``, solves for and
        returns the coefficients of the spherical Bessel functions in
        each shell.  The even and odd elements are the coefficients of
        :math:`j` and :math:`y`, respectively."""
        n = len(self.c)   # number of components
        N = 2*(n-1)       # matrix size, for convenience

        # x = [α₂, β₂, α₃, β₃…]
        A = np.zeros((N,N))
        b = np.zeros(N)

        # first and second rows are match to F₁ = j(ωr/c[1]) at R₁
        b[0] = j(l,omega*self.R[0]/self.c[0])
        b[1] = j(l,omega*self.R[0]/self.c[0], derivative=True)
        A[0,0] = j(l,omega*self.R[0]/self.c[1])
        A[0,1] = y(l,omega*self.R[0]/self.c[1])
        A[1,0] = j(l,omega*self.R[0]/self.c[1], derivative=True)
        A[1,1] = y(l,omega*self.R[0]/self.c[1], derivative=True)
    
        for i in range(2,N,2):
            # i is matrix row number, k is R boundary number
            k = i//2
            A[i,i-2] = -j(l,omega*self.R[k]/self.c[k])
            A[i,i-1] = -y(l,omega*self.R[k]/self.c[k])
            A[i,i]   =  j(l,omega*self.R[k]/self.c[k+1])
            A[i,i+1] =  y(l,omega*self.R[k]/self.c[k+1])
            A[i+1,i-2] = -j(l,omega*self.R[k]/self.c[k], derivative=True)
            A[i+1,i-1] = -y(l,omega*self.R[k]/self.c[k], derivative=True)
            A[i+1,i]   =  j(l,omega*self.R[k]/self.c[k+1], derivative=True)
            A[i+1,i+1] =  y(l,omega*self.R[k]/self.c[k+1], derivative=True)

        return np.linalg.solve(A, b)
