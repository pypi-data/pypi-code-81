"""AtomRhoOrbitalRadialSlater and AtomRhoOrbitalRadialSlaterL classes."""

from typing import NoReturn
import os
import os.path
import math
import numpy
import scipy
import scipy.optimize
from pycifstar import to_data

from cryspy.A_functions_base.function_1_rhocif import transs, calc_GCF

from cryspy.B_parent_classes.cl_1_item import ItemN
from cryspy.B_parent_classes.cl_2_loop import LoopN

from cryspy.C_item_loop_classes.cl_1_atom_type_scat import AtomTypeScat


class AtomRhoOrbitalRadialSlater(ItemN):
    """Description of radial Slater functions.

    These items are used when the radial dependence of the
    electron density, R(k(l), l, r), of the atom specified in
    _atom_rho_orbital_atom_label is expressed as a Slater-type
    function [Hansen & Coppens (1978), equation (3)]:

    Attributes
        - n0, zeta0 (mandatory)
        - coeff_1s, coeff_2s, coeff_3s, coeff_4s, coeff_5s, coeff_2p,
          coeff_3p, coeff_4p, coeff_5p, coeff_3d, coeff_4d, coeff_5d,
          coeff_4f, coeff_5f (optional)
    """

    ATTR_MANDATORY_NAMES = ("n0", "zeta0")
    ATTR_MANDATORY_TYPES = (int, float)
    ATTR_MANDATORY_CIF = ("n0", "zeta0")

    ATTR_OPTIONAL_NAMES = (
        "coeff_1s", "coeff_2s", "coeff_3s", "coeff_4s", "coeff_5s", "coeff_2p",
        "coeff_3p", "coeff_4p", "coeff_5p", "coeff_3d", "coeff_4d", "coeff_5d",
        "coeff_4f", "coeff_5f")
    ATTR_OPTIONAL_TYPES = (float, float, float, float, float, float, float,
                           float, float, float, float, float, float, float)
    ATTR_OPTIONAL_CIF = (
        "coeff_1s", "coeff_2s", "coeff_3s", "coeff_4s", "coeff_5s", "coeff_2p",
        "coeff_3p", "coeff_4p", "coeff_5p", "coeff_3d", "coeff_4d", "coeff_5d",
        "coeff_4f", "coeff_5f")

    ATTR_NAMES = ATTR_MANDATORY_NAMES + ATTR_OPTIONAL_NAMES
    ATTR_TYPES = ATTR_MANDATORY_TYPES + ATTR_OPTIONAL_TYPES
    ATTR_CIF = ATTR_MANDATORY_CIF + ATTR_OPTIONAL_CIF

    ATTR_INT_NAMES = ()
    ATTR_INT_PROTECTED_NAMES = ()

    # parameters considered are refined parameters
    ATTR_REF = ("zeta0", "coeff_1s", "coeff_2s", "coeff_3s", "coeff_4s",
                "coeff_5s", "coeff_2p", "coeff_3p", "coeff_4p", "coeff_5p",
                "coeff_3d", "coeff_4d", "coeff_5d", "coeff_4f", "coeff_5f")
    ATTR_SIGMA = tuple([f"{_h:}_sigma" for _h in ATTR_REF])
    ATTR_CONSTR_FLAG = tuple([f"{_h:}_constraint" for _h in ATTR_REF])
    ATTR_REF_FLAG = tuple([f"{_h:}_refinement" for _h in ATTR_REF])

    # constraints on the parameters
    D_CONSTRAINTS = {}

    # default values for the parameters
    D_DEFAULT = {}
    for key in ATTR_SIGMA:
        D_DEFAULT[key] = 0.
    for key in (ATTR_CONSTR_FLAG + ATTR_REF_FLAG):
        D_DEFAULT[key] = False

    PREFIX = "atom_rho_orbital_radial_Slater"

    def __init__(self, **kwargs) -> NoReturn:
        super(AtomRhoOrbitalRadialSlater, self).__init__()

        # defined for any integer and float parameters
        D_MIN = {"n0": 0, "zeta0": 0.}

        # defined for ani integer and float parameters
        D_MAX = {}

        self.__dict__["D_MIN"] = D_MIN
        self.__dict__["D_MAX"] = D_MAX
        for key, attr in self.D_DEFAULT.items():
            setattr(self, key, attr)
        for key, attr in kwargs.items():
            setattr(self, key, attr)

    def calc_normalized_rho(self, radius: numpy.array, kappa: float = 1.) -> \
            numpy.array:
        """Give normalized Slatter type function.

        R = ((2*zeta0)**(n0+0.5)/((2*n0)!)**0.5)*r**(n0-1)*exp(-zeta0*r)
        (see Clementi_1974)

        Arguments
        ---------
            - radius is numpy 1D array of float numbers in Angstrem
            - kappa is describes contraction/extension of atomic orbital

        Output
        ------
            - normalized radial density given as numpy 1D array of floats

        Example
        -------
            >>> radius = numpy.linspace(0.,5,600)
            >>> rho = obj.calc_normalized_rho(radius)
        """
        # transformation from atomic units to inverse angstrems
        zeta0 = self.zeta0
        n0 = self.n0
        zeta_ang = kappa*zeta0/0.52918
        coeff_norm = ((2.*zeta_ang)**(float(n0)+0.5)) / \
            math.sqrt(math.factorial(2*n0))
        norm_density = coeff_norm*(radius**(n0-1))*numpy.exp(-zeta_ang*radius)
        return norm_density

    def calc_jl(self, sthovl: numpy.array, l_max: int, kappa: float = 1.) -> \
            numpy.array:
        """Calculate jl for l from 0 until l_max of atomic orbital."""
        zeta0 = self.zeta0
        n0 = self.n0
        zeta_ang = kappa*zeta0/0.52918
        coeff_norm = ((2.*zeta_ang)**(float(n0)+0.5)) / \
            math.sqrt(math.factorial(2*n0))
        nn, zeta = (n0+n0), (zeta_ang+zeta_ang)
        q = 4.*numpy.pi*sthovl
        q_2d, l_2d = numpy.meshgrid(q, range(l_max+1), indexing="ij")
        ql_2d = numpy.power(q_2d, l_2d)
        jl = ql_2d*coeff_norm*coeff_norm*transs(l_max, nn, zeta, sthovl)
        return jl


class AtomRhoOrbitalRadialSlaterL(LoopN):
    """Description of radial Slater functions.

    These items are used when the radial dependence of the
    electron density, R(k(l), l, r), of the atom specified in
    _atom_rho_orbital_atom_label is expressed as a Slater-type
    function [Hansen & Coppens (1978), equation (3)]:
    """

    ITEM_CLASS = AtomRhoOrbitalRadialSlater
    ATTR_INDEX = "atom_label"

    def __init__(self, loop_name: str = None) -> NoReturn:
        super(AtomRhoOrbitalRadialSlaterL, self).__init__()
        self.__dict__["items"] = []
        self.__dict__["loop_name"] = loop_name

    def calc_normalized_rho(self, radius: numpy.array, shell: str, kappa=1.,
                            *argv) -> numpy.array:
        """Calc normalized rho.

        Give normalized Slatter type function at given radius for given shell.

        $$
        R = sum_i coeff_i*((2*zeta0)**(n0+0.5)/(2*n0)!)*r**(n0-1)*exp(-zeta0*r)
        $$
        (see Clementi_1974)

        Arguments
        ---------
            - radius is numpy 1D array of float numbers in Angstrem
            - shell is it is orbital shell
            - kappa is describes contraction/extension of atomic orbital

        Output
        ------
            - normalized radial density given as numpy 1D array of floats

        Example
        -------
            >>> radius = numpy.linspace(0.,5,600)
            >>> rho = obj.calc_rho(radius, "3d")
            >>> rho = obj.calc_rho(radius, "3d", "2s")
        """
        # transformation from atomic units to inverse angstrems
        l_shell = [shell]
        l_shell.extend(argv)
        n_shell = len(l_shell)
        n_item = len(self.items)
        coeff = numpy.zeros((n_shell, n_item), dtype=float)

        norm_density = numpy.zeros((radius.size, n_shell), dtype=float)

        l_attr = [f"coeff_{_.strip():}" for _ in l_shell]
        for _i, _item in enumerate(self.items):
            normalized_rho = _item.calc_normalized_rho(radius, kappa=kappa)
            for _j, _attr in enumerate(l_attr):
                coeff[_j, _i] = float(getattr(_item, _attr))
            norm_density += normalized_rho[:, numpy.newaxis] * \
                (coeff[:, _i])[numpy.newaxis, :]
        return norm_density

    @classmethod
    def take_objects_for_atom_type(cls, atom_type: str) -> list:
        """Take objects for atom type."""
        l_arors = []
        f_dir = os.path.dirname(__file__)
        f_name = os.path.join(f_dir, "library.rcif")

        obj_rcif = to_data(f_name)
        s_atom_type = ("".join([_ for _ in atom_type if _.isalpha()])).lower()
        for loop in obj_rcif.loops:
            loop_rcif = cls.from_cif(str(loop))
            if loop_rcif is not None:
                s_loop_name = loop_rcif.loop_name
                s_atom_type_loop = (s_loop_name.split("_")[0]).lower()
                if s_atom_type_loop == s_atom_type:
                    l_arors.append(loop_rcif)
        return l_arors

    def calc_jl_by_radial_density(self, sthovl, lmax: int, shell: str,
                                  kappa=1.):
        """Calculate <j_l> for given sthovl, l and shell.

        $$
        <j_l> = sum_{n, dzeta} integral_{0}^{inf} R^{2}(n,dzeta,r) j_l(r*s) dr
        $$
        """
        n0 = numpy.array(self.n0, dtype=int)
        zeta0 = numpy.array(self.zeta0, dtype=float)
        coeff_h = getattr(self, f"coeff_{shell:}")

        coeff = numpy.array([_.value for _ in coeff_h], dtype=float)

        if any([_ is None for _ in coeff]):
            return None

        np_q = 4*numpy.pi * sthovl
        np_q = 2*sthovl

        np_l = numpy.array(range(lmax+1), dtype=int)
        np_q_2d, np_l_2d = numpy.meshgrid(np_q, np_l, indexing="ij")
        np_ql_2d = numpy.power(np_q_2d, np_l_2d)

        jl = np_ql_2d * calc_GCF(n0, zeta0, coeff, kappa,
                                 n0, zeta0, coeff, kappa,
                                 sthovl, lmax)
        return jl

    def refine_coefficients_by_jl(self, atom_type: str, shell: str,
                                  sthovl_min=0.0, sthovl_max=2.0, lande=2.,
                                  kappa=1., sthvl_num=100):
        """Refine coefficients by jl."""
        ats = AtomTypeScat.form_by_symbol(atom_type)

        sthovl = numpy.linspace(sthovl_min, sthovl_max, num=int(sthvl_num))
        ff = ats.calc_form_factor(sthovl, lande=lande, kappa=kappa)
        fitable = self.get_variables()

        def tempfunc(param):
            for _1, _2 in zip(fitable, param):
                _1.value = abs(_2)  # only positive coefficients
            j0 = self.calc_jl_by_radial_density(sthovl, 0, shell, kappa)[0]
            chi_sq = (numpy.square(ff - j0)).sum()
            return chi_sq

        param_0 = [_.value for _ in fitable]
        j0 = self.calc_jl_by_radial_density(sthovl, 0, shell, kappa)[0]

        res = scipy.optimize.basinhopping(tempfunc, param_0, niter=10,
                                          T=0.1, stepsize=0.1, interval=20,
                                          disp=True)
        for _1, _2 in zip(fitable, res.x):
            _1.value = abs(_2)  # only positive coefficients, found minima

        return res

# s_cont = """
# loop_V_s
# _atom_rho_orbital_radial_slater_n0
# _atom_rho_orbital_radial_slater_zeta0
# _atom_rho_orbital_radial_slater_coeff_1s
# _atom_rho_orbital_radial_slater_coeff_2s
# _atom_rho_orbital_radial_slater_coeff_3s
# _atom_rho_orbital_radial_slater_coeff_4s
#     1 22.77630  0.95175 -0.29620  0.10614 -0.02339
#     1 36.05340  0.02115  0.00019  0.00042 -0.00046
#     2 19.54100  0.03441 -0.15795  0.06539 -0.01626
#     2  9.37400  0.00415 10.04067 -0.42093  0.09958
#     3  7.90503 -0.00366  0.12576 -0.25395  0.05408
#     3  5.12985  0.00552 -0.02332  0.73273 -0.11001

#   """

# obj = AtomRhoOrbitalRadialSlaterL.from_cif(s_cont)
# obj = AtomRhoOrbitalRadialSlaterL.take_objects_for_atom_type("O")
# print(obj, end="\n\n")
