import logging
import sys
import numpy as np
from scipy.sparse import csr_matrix
from patsy import dmatrix
import sympy


def _leg_mt(time, tmax, tmin, order):
    time = np.array(time, dtype=float).reshape(-1, 1)
    tvec = 2 * (time - tmin) / (tmax - tmin) - 1
    pmat = []
    for k in range(order + 1):
        c = int(k / 2)
        j = k
        p = 0
        for r in range(0, c + 1):
            p += np.sqrt((2 * j + 1.0) / 2.0) * pow(0.5, j) * (pow(-1, r) *
                np.math.factorial(2 * j - 2 * r) / (np.math.factorial(r) *
                np.math.factorial(j - r) * np.math.factorial(j - 2 * r))) * pow(tvec, j - 2 * r)
        p = np.array(p)
        pmat.append(p)
    return pmat


def _design_matrix(formula, data_df):
    """
    Build the design matrix
    :param formula:  An object that can be used to construct a design matrix. See patsy.dmatrix for detail.
    :param data_df: Pandas data frame
    :return: full rank design matrix
    """
    dmat = dmatrix(formula, data_df)
    dmat = np.asarray(dmat)
    return dmat


def _design_matrix_crank(formula, data_df):
    """
    Build the design matrix
    :param formula:  An object that can be used to construct a design matrix. See patsy.dmatrix for detail.
    :param data_df: Pandas data frame
    :return: design matrix, full rank design matrix, the indexes for the linear independent columns, label of design matrix
    """
    dmat = dmatrix(formula, data_df)
    col_arr = repr(dmat).split("\n")[1].split('\s+')
    dmat = np.asarray(dmat)
    _, indexes = sympy.Matrix(dmat).rref()
    dmat_full_rank = dmat[:, indexes]
    return dmat, dmat_full_rank, indexes, col_arr
