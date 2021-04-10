import numpy as np
import pandas as pd
from scipy import linalg
from scipy import sparse
from scipy.sparse import csr_matrix, hstack, block_diag
from scipy.stats import chi2
import datetime
import gc
import logging
from tqdm import tqdm
from patsy import dmatrix
from functools import reduce
import random
import sympy


from gmat.process_plink.process_plink import impute_geno
from pysnptools.snpreader import Bed
from ._pre_data import _pre_data
from ._common import _design_matrix, _leg_mt


def unbalance_longwas_fixed_permutation(data_file, id, tpoint, trait, bed_file, agmat_file, var_com, permutation_lst=None,
            snp_lst=None, tfix=None, fix=None, forder=3, aorder=3, porder=3, na_method='omit', crank=False,
                             prefix_outfile='unbalance_longwas_fixed_permutation'):
    """
    the longitudinal GWAS for the unbalanced data treating the SNP as the time varied fixed effect.
    :param data_file: the data file. The first row is the variate names whose first initial position is alphabetical.
    For the class variates, the first letter must be capital; for the covariates (continuous variates), the first letter
    must be lowercase.
    :param id: A class variate name which indicates the individual id column in the data file.
    :param tpoint: A covariate names which indicates the time point column in the data file.
    :param trait: A variate name which indicates the analyzed trait column in the data file.
    :param bed_file: the prefix for the plink binary file.
    :param agmat_file: the file for genomic relationship matrix. This file can be produced by
    gmat.gmatrix.agmat function using agmat(bed_file, inv=True, small_val=0.001, out_fmt='id_id_val')
    :param var_com: the estimated variance parameters by the gmat.longwas.unbalance.unbalance_varcom function.
    :param permutation_lst: the index list for permutation. Default is None ([0, 1000)].
    :param snp_lst: the snp list to test. Default is None.
    :param tfix: A class variate name for the time varied fixed effect. Default value is None. Only one time varied
    fixed effect can be included in the current version.
    :param fix: Expression for the time independent fixed effect. Default value is None. An example:
    fix = "Sex + age + Season".
    :param forder: the order of Legendre polynomials for the time varied fixed effect. The default value is 3.
    :param aorder: the order of Legendre polynomials for the additive genetic effect. The default value is 3.
    :param porder: the order of Legendre polynomials for the permanent environment effect. The default value is 3.
    :param na_method: The method to deal with missing values. The default value is 'omit'. 'omit' method will delete the
    row with missing values. 'include' method will fill the missing values with the adjacent values.
    :param crank: force the column full rank of fixed effects. Default is False.
    :param prefix_outfile: the prefix for the output file. Default is 'unbalance_longwas_fixed'.
    :return: A pandas data frame for the test result.
    """
    logging.info('################################')
    logging.info('###Prepare the related matrix###')
    logging.info('################################')
    if var_com.shape[0] != aorder*(aorder+1)/2 + aorder + 1 + porder*(porder+1)/2 + porder + 1 + 1:
        logging.error('ERROR: Variances do not match the data, please check')
        sys.exit()
    data_df, ag, id_code, id_order = _pre_data(data_file, id, tpoint, trait, agmat_file, na_method=na_method)
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
            mat.append(xmat_t * dmat_t[:, i:(i + 1)])
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
    add_mat = csr_matrix((val, (row, col)), shape=(data_df.shape[0], ag.shape[0]))
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

    logging.info('***Calculate the phenotypic (co)variance and P matrix***')
    eff_ind = [[0, xmat.shape[1]]]
    for i in range(len(zmat)):
        temp = [eff_ind[i][-1]]
        for j in range(len(zmat[i])):
            temp.append(temp[-1] + zmat[i][j].shape[1])
        eff_ind.append(temp)
    zmat_con_lst = [hstack(zmat[0]), hstack(zmat[1])]  # combined random matrix

    def cal_cov(var_ind, var_com):
        """
        return the matrix format of covariance.
        """
        cov_df = var_com.loc[var_com.loc[:, 'var']==var_ind, :]
        row = np.array(cov_df['vari']) - 1
        col = np.array(cov_df['varj']) - 1
        val = cov_df['var_com']
        cov_mat = csr_matrix((val, (row, col))).toarray()
        cov_mat = cov_mat + np.tril(cov_mat, k=-1).T
        return cov_mat
    add_cov = cal_cov(1, var_com)
    per_cov = cal_cov(2, var_com)
    res_var = np.array(var_com['var_com'])[-1]
    vmat = zmat_con_lst[0].dot((zmat_con_lst[0].dot(np.kron(add_cov, ag))).T)
    one_id = sparse.eye(zmat_con_lst[1].shape[1]/per_cov.shape[0])
    vmat = vmat + zmat_con_lst[1].dot((zmat_con_lst[1].dot(sparse.kron(per_cov, one_id))).T)
    vmat_diag = np.diag(vmat) + res_var
    np.fill_diagonal(vmat, vmat_diag)
    vmat = linalg.inv(vmat)
    xv = np.dot(xmat.T, vmat)
    xvx = np.dot(xv, xmat)
    xvx = linalg.inv(xvx)
    pmat = vmat - reduce(np.dot, [xv.T, xvx, xv])
    logging.info('***Read the snp data***')
    snp_on_disk = Bed(bed_file, count_A1=False)
    num_id = snp_on_disk.iid_count
    num_snp = snp_on_disk.sid_count
    logging.info("There are {:d} individuals and {:d} SNPs.".format(num_id, num_snp))
    fam_df = pd.read_csv(bed_file + '.fam', sep='\s+', header=None)
    id_geno = list(np.array(fam_df.iloc[:, 1], dtype=str))
    id_order_index = []
    for i in id_order:
        id_order_index.append(id_geno.index(i))
    if snp_lst is None:
        snp_lst = range(num_snp)
    snp_lst = list(snp_lst)
    if min(snp_lst) < 0 or max(snp_lst) >= num_snp:
        logging.info('The value in the snp list should be >= {} and < {}', 0, num_snp)
        exit()
    snp_mat = snp_on_disk[id_order_index, snp_lst].read().val
    if np.any(np.isnan(snp_mat)):
        logging.info('Missing genotypes are imputed with random genotypes.')
        snp_mat = impute_geno(snp_mat)
    logging.info('#####################################################################')
    logging.info('###Start the fixed regression longitudinal GWAS for unbalance data###')
    logging.info('#####################################################################')
    leg_lst = []  # legendre polynomials for time dependent fixed SNP effects, save for each individuals
    for val in id_order:
        leg_val = _leg_mt(data_df[data_df[id] == val][tpoint], tmax, tmin, forder)
        leg_val = np.concatenate(leg_val, axis=1)
        leg_lst.append(leg_val)
    # leg_mat = block_diag(leg_lst, format='csr')
    tpoint_vec = sorted(set(data_df[tpoint]))
    leg_tpoint_mat = _leg_mt(np.array(tpoint_vec), tmax, tmin, forder)
    leg_tpoint_mat = np.concatenate(leg_tpoint_mat, axis=1)
    leg_tpoint_accum = np.sum(leg_tpoint_mat, axis=0)
    chi_df = leg_lst[0].shape[1]
    if permutation_lst is None:
        permutation_lst = range(1000)
    id_perm = list(range(len(id_order)))
    for rep in permutation_lst:
        logging.info("***Permutation: {} ***".format(rep))
        random.shuffle(id_perm)
        snp_mat = snp_mat[id_perm, :]
        eff_vec = []
        chi_vec = []
        p_vec = []
        p_min_vec = []
        eff_accum_vec = []
        p_accum_vec = []
        eff_tpoint_mat = []
        p_tpoint_mat = []
        # eye_forder = sparse.eye(forder + 1, format="csr")
        for i in tqdm(range(snp_mat.shape[1])):
            snp_fix = list(map(lambda x, y: x * y, leg_lst, list(snp_mat[:, i])))
            snp_fix = np.concatenate(snp_fix, axis=0)
            # snp_fix = leg_mat.dot((sparse.kron(snp_mat[:, i:(i+1)], eye_forder)))
            # snp_fix = snp_fix.toarray()
            p_xsnp = np.dot(pmat, snp_fix)
            xpx = np.dot(snp_fix.T, p_xsnp)
            xpx = linalg.inv(xpx)
            xpy = np.dot(p_xsnp.T, y)
            b = np.dot(xpx, xpy)
            eff = b[-chi_df:, -1]
            eff_var = xpx[-chi_df:, -chi_df:]
            chi_val = np.sum(np.dot(np.dot(eff.T, linalg.inv(eff_var)), eff))
            p_val = chi2.sf(chi_val, chi_df)
            eff_vec.append(eff)
            chi_vec.append(chi_val)
            p_vec.append(p_val)
            eff_tpoint_vec = []
            p_tpoint_vec = []
            for k in range(leg_tpoint_mat.shape[0]):
                eff_tpoint = np.sum(np.dot(leg_tpoint_mat[k, :], eff))
                eff_tpoint_vec.append(eff_tpoint)
                eff_var_tpoint = np.sum(np.dot(leg_tpoint_mat[k, :], np.dot(eff_var, leg_tpoint_mat[k, :])))
                chi_tpoint = eff_tpoint * eff_tpoint / eff_var_tpoint
                p_tpoint = chi2.sf(chi_tpoint, 1)
                p_tpoint_vec.append(p_tpoint)
            eff_tpoint_mat.append(np.array(eff_tpoint_vec).reshape(1, -1))
            p_tpoint_mat.append(np.array(p_tpoint_vec).reshape(1, -1))
            p_min_vec.append(min(p_tpoint_vec))
            eff_accum = np.sum(np.dot(leg_tpoint_accum, eff))
            eff_accum_vec.append(eff_accum)
            eff_var_accum = np.sum(np.dot(leg_tpoint_accum, np.dot(eff_var, leg_tpoint_accum)))
            chi_accum = eff_accum * eff_accum / eff_var_accum
            p_accum = chi2.sf(chi_accum, 1)
            p_accum_vec.append(p_accum)
        logging.info('Finish association analysis')
        logging.info('***Output***')
        head_tpoint = []
        for val in tpoint_vec:
            head_tpoint.append('eff_tpoint_' + str(val))
        for val in tpoint_vec:
            head_tpoint.append('p_tpoint_' + str(val))
        eff_tpoint_mat = np.concatenate(eff_tpoint_mat, axis=0)
        p_tpoint_mat = np.concatenate(p_tpoint_mat, axis=0)
        res_tpoint = np.concatenate([eff_tpoint_mat, p_tpoint_mat], axis=1)
        np.savetxt(prefix_outfile + '.tpoint.{}'.format(rep), res_tpoint, header='\t'.join(head_tpoint), delimiter="\t", comments='')
        snp_info_file = bed_file + '.bim'
        snp_info = pd.read_csv(snp_info_file, sep='\s+', header=None)
        res_df = snp_info.iloc[snp_lst, [0, 1, 3, 4, 5]]
        res_df.columns = ['chro', 'snp_ID', 'pos', 'allele1', 'allele2']
        res_df.loc[:, 'order'] = snp_lst
        res_df = res_df.iloc[:, [5, 0, 1, 2, 3, 4]]
        eff_vec = np.array(eff_vec)
        for i in range(eff_vec.shape[1]):
            col_ind = 'eff' + str(i)
            res_df.loc[:, col_ind] = eff_vec[:, i]
        res_df.loc[:, 'eff_accum'] = eff_accum_vec
        res_df.loc[:, 'chi_val'] = chi_vec
        res_df.loc[:, 'p_val'] = p_vec
        res_df.loc[:, 'p_min'] = p_min_vec
        res_df.loc[:, 'p_accum'] = p_accum_vec
        out_file = prefix_outfile + '.res.{}'.format(rep)
        res_df.to_csv(out_file, sep='\t', index=False)
    return 0
