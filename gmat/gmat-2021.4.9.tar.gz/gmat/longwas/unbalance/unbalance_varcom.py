import logging
from scipy import sparse
from scipy.sparse import csr_matrix, hstack
import numpy as np
from scipy import linalg
import pandas as pd
from patsy import dmatrix
import sympy
import gc
import os

from ._pre_data import _pre_data
from ._common import _design_matrix, _leg_mt
from ._emai import _emai


def unbalance_varcom(data_file, id, tpoint, trait, agmat_file, tfix=None, fix=None, forder=3, aorder=3, porder=3,
             na_method='omit', init=None, maxiter=100, cc_par=1.0e-8, cc_gra=1.0e-3, crank=False,
                     em_weight_step=0.01, out_file='unbalance_varcom'):
    """
    Estimate the variance parameters for the unbalance longitudinal data using the random regression model
    :param data_file: the data file. The first row is the variate names whose first initial position is alphabetical.
    For the class variates, the first letter must be capital; for the covariates (continuous variates), the first letter
    must be lowercase.
    :param id: A class variate name which indicates the individual id column in the data file.
    :param tpoint: A covariate names which indicates the time point column in the data file.
    :param trait: A variate name which indicates the analyzed trait column in the data file.
    :param agmat_file: the prefix for genomic relationship matrix file. This file can be produced by
    gmat.gmatrix.agmat function using agmat(bed_file, out_fmt='id_id_val')
    :param tfix: variate names for the time varied fixed effect. Default value is None. An example:
    tfix = "Sex + age + Season".
    :param fix: Expression for the time independent fixed effect. Default value is None. An example:
    fix = "Sex + age + Season".
    :param forder: the order of Legendre polynomials for the time varied fixed effect. The default value is 3.
    :param aorder: the order of Legendre polynomials for the additive genetic effect. The default value is 3.
    :param porder: the order of Legendre polynomials for the permanent environment effect. The default value is 3.
    :param na_method: The method to deal with missing values. The default value is 'omit'. 'omit' method will delete the
    row with missing values. 'include' method will fill the missing values with the adjacent values.
    :param init: the initial values for the variance parameters. The default value is None.
    :param maxiter: the maximum number of iteration. Default is 100.
    :param cc_par: Convergence criteria for the changed variance parameters. Default is 1.0e-8.
    :param cc_gra: Convergence criteria for the norm of gradient vector. Default is 1.0e-3.
    :param crank: force the column full rank of fixed effects. Default is False.
    :param em_weight_step: the step of the em weight. Default is 0.001.
    :param out_file: the prefix for the output file. Default is 'unbalance_varcom'.
    :return: the estimated variance parameters.
    """
    logging.info('########################################################################')
    logging.info('###Prepare the data for unbalanced longitudinal variances estimation.###')
    logging.info('########################################################################')
    logging.info('***Read the data file and genomic relationship matrix***')
    data_df, ag, id_code, _ = _pre_data(data_file, id, tpoint, trait, agmat_file, na_method=na_method)
    ag_inv = linalg.inv(ag)
    del ag
    gc.collect()
    logging.info('***Build the design matrix for fixed effect***')
    logging.info('Time dependent fixed effect: {}'.format(tfix))
    tmin = np.min(data_df[tpoint])
    tmax = np.max(data_df[tpoint])
    xmat_t = _leg_mt(data_df[tpoint], tmax, tmin, forder)
    xmat_t = np.concatenate(xmat_t, axis=1)
    if tfix is not None:
        mat = []
        dmat_t = _design_matrix(tfix, data_df)
        for i in range(dmat_t.shape[1]):
            mat.append(xmat_t * dmat_t[:, i:(i+1)])
        xmat_t = np.concatenate(mat, axis=1)
        del mat, dmat_t
        gc.collect()
    logging.info('Time independent fixed effect: {}'.format(fix))
    xmat = xmat_t
    if fix is not None:
        xmat_nt = _design_matrix(fix, data_df)
        xmat = np.concatenate([xmat_t, xmat_nt[:, 1:]], axis=1)
    if crank:
        _, indexes = sympy.Matrix(xmat).rref()
        xmat = xmat[:, indexes]
    logging.info('***Build the dedign matrix for random effect***')
    logging.info('Legendre order for additive effects: {}'.format(aorder))
    leg_add = _leg_mt(data_df[tpoint], tmax, tmin, aorder)
    row = np.array(range(data_df.shape[0]))
    col = np.array(id_code)
    val = np.array([1.0] * data_df.shape[0])
    add_mat = csr_matrix((val, (row, col)), shape=(data_df.shape[0], ag_inv.shape[0]))
    zmat_add = []
    for i in range(len(leg_add)):
        zmat_add.append(add_mat.multiply(leg_add[i]))
    logging.info('Legendre order for permanent environmental effect: {}'.format(porder))
    leg_per = _leg_mt(data_df[tpoint], tmax, tmin, porder)
    per_mat = csr_matrix((val, (row, col)))
    zmat_per = []
    for i in range(len(leg_per)):
        zmat_per.append((per_mat.multiply(leg_per[i])))
    del row, col, val, leg_add, add_mat, leg_per, per_mat
    gc.collect()
    zmat = [zmat_add, zmat_per]
    y = np.array(data_df[trait]).reshape(-1, 1)
    logging.info('###########################################################')
    logging.info('###Start the unbalanced longitudinal variances estimation###')
    logging.info('###########################################################')
    res = _emai(y, xmat, zmat, ag_inv, init=init, maxiter=maxiter, cc_par=cc_par, cc_gra=cc_gra, em_weight_step=em_weight_step,
          out_file=out_file)
    var_file = out_file + '.var'
    res.to_csv(var_file, sep='\t', index=False)
    return res
