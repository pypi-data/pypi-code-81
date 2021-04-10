import sys
import math
import numpy as np
import pandas as pd
from scipy import linalg
from scipy import sparse
from scipy.sparse import csr_matrix, isspmatrix, hstack, vstack
import datetime
import logging


def _emai(y, xmat, zmat, ag_inv, init=None, maxiter=30, cc_par=1.0e-8, cc_gra=1.0e-6, em_weight_step=0.01,
          out_file='unbalance_varcom'):
    def init_var(cov_dim):
        """
        initialize the variances
        """
        y_var = np.var(y)/(cov_dim[0] + cov_dim[1] + 1)
        add_cov = np.diag([y_var]*cov_dim[0])
        add_ind = np.tril_indices_from(add_cov)
        per_cov = np.diag([y_var]*cov_dim[1])
        per_ind = np.tril_indices_from(per_cov)
        cov_ind = [1] * len(add_ind[0]) + [2] * len(per_ind[0]) + [3]
        cov_ind_i = list(add_ind[0] + 1) + list(per_ind[0] + 1) + [1]
        cov_ind_j = list(add_ind[1] + 1) + list(per_ind[1] + 1) + [1]
        var_com = list(add_cov[add_ind]) + list(per_cov[per_ind]) + [y_var]
        var_df = {'var': cov_ind,
                  "vari": cov_ind_i,
                  "varj": cov_ind_j,
                  "var_com": var_com}
        var_df = pd.DataFrame(var_df, columns=['var', "vari", "varj", "var_com"])
        return np.array(var_com), var_df
    cov_dim = [len(zmat[0]), len(zmat[1])]  # the dimension for the covariance matrix
    var_com, var_df = init_var(cov_dim)
    if init is not None:
        if len(var_com) != len(init):
            logging.error('The length of initial variances should be {}'.format(len(var_com)))
            sys.exit()
        else:
            var_com = np.array(init)
            var_df['var_com'] = var_com

    def effect_index():
        """
        return the vector of indexes for all effects
        """
        eff_ind = [[0, xmat.shape[1]]]
        for i in range(len(zmat)):
            temp = [eff_ind[i][-1]]
            for j in range(len(zmat[i])):
                temp.append(temp[-1] + zmat[i][j].shape[1])
            eff_ind.append(temp)
        return eff_ind
    eff_ind = effect_index()

    logging.info('***prepare the MME***')
    zmat_con_lst = [hstack(zmat[0]), hstack(zmat[1])]  # combined random matrix
    zmat_con = hstack(zmat_con_lst)  # design matrix for random effects
    wmat = hstack([xmat, zmat_con])  # merged design matrix
    cmat_pure = np.dot(wmat.T, wmat)  # C matrix
    rhs_pure = wmat.T.dot(y)  # right hand
    logging.info('initialize the variate')
    num_record = y.shape[0]
    iter_count = 0
    cc_par_val = 1000.0
    cc_gra_val = 1000.0
    delta = 1000.0
    var_com_update = var_com * 1000
    logging.info("initial variances: {}".format(var_df))

    def pre_cov_inv(cov_dim, var_com):
        """
        return the inversion of covariance matrix. If one covariance matrix is not positive, return None.
        """
        cov_inv = []  # the inversion of covariance matrix list
        if var_com[-1] <= 0:
            return None
        for i in range(len(cov_dim)):
            covar = np.zeros((cov_dim[i], cov_dim[i]))
            covar[np.tril_indices(cov_dim[i])] = np.array(var_df[var_df['var']==(i+1)].iloc[:, -1])
            covar = np.add(covar, np.tril(covar, -1).T)
            try:
                linalg.cholesky(covar)
            except:
                return None
            covar = linalg.inv(covar)
            cov_inv.append(covar)
        return cov_inv
    cov_inv = pre_cov_inv(cov_dim, var_com)
    # cov_inv = pre_covi_mat(cov_dim, var_com_update)
    if cov_inv is None:
        logging.error("ERROR: Initial variances is not positive define, please check!")
        sys.exit()

    def cal_cmat_inv(cmat):
        """
        return the inversion of coefficient matrix
        """
        cmat[eff_ind[1][0]:eff_ind[1][-1], eff_ind[1][0]:eff_ind[1][-1]] = \
            cmat[eff_ind[1][0]:eff_ind[1][-1], eff_ind[1][0]:eff_ind[1][-1]] + linalg.kron(cov_inv[0], ag_inv)
        cmat[eff_ind[2][0]:eff_ind[2][-1], eff_ind[2][0]:eff_ind[2][-1]] = \
            cmat[eff_ind[2][0]:eff_ind[2][-1], eff_ind[2][0]:eff_ind[2][-1]] + \
            sparse.kron(cov_inv[1], sparse.eye(ag_inv.shape[0], format="csr"))
        cmat_inv = linalg.inv(cmat)
        return cmat_inv

    def cal_fd_mat(cmat):
        """
        Calculate the first-order derivative
        """
        fd_mat = []
        # addtive part
        qnum = zmat_con_lst[0].shape[1] / cov_dim[0]
        tmat = np.zeros((cov_dim[0], cov_dim[0]))
        eff_lst = []
        for j in range(cov_dim[0]):
            for k in range(j + 1):
                tmat[j, k] = np.sum(np.multiply(ag_inv, cmat[eff_ind[1][j]:eff_ind[1][j + 1],
                                                        eff_ind[1][k]:eff_ind[1][k + 1]]))
                tmat[k, j] = tmat[j, k]
            eff_lst.append(eff[eff_ind[1][j]:eff_ind[1][j + 1], :])
        eff_mat = np.dot(np.concatenate(eff_lst, axis=1), cov_inv[0])
        fd_val = qnum * cov_inv[0] - np.dot(np.dot(cov_inv[0], tmat), cov_inv[0]) - np.dot(np.dot(eff_mat.T, ag_inv), eff_mat)
        fd_val[np.tril_indices(cov_dim[0], k=-1)] = 2.0 * fd_val[np.tril_indices(cov_dim[0], k=-1)]
        fd_mat.extend(list(-0.5 * fd_val[np.tril_indices(cov_dim[0], k=0)]))
        # per part
        eff_lst = []
        per_kin = sparse.eye(ag_inv.shape[0], format="csr")
        for j in range(cov_dim[1]):
            for k in range(j + 1):
                tmat[j, k] = np.sum(per_kin.multiply(cmat[eff_ind[2][j]:eff_ind[2][j + 1],
                                                    eff_ind[2][k]:eff_ind[2][k + 1]]))
                tmat[k, j] = tmat[j, k]
            eff_lst.append(eff[eff_ind[2][j]:eff_ind[2][j + 1], :])
        eff_mat = np.dot(np.concatenate(eff_lst, axis=1), cov_inv[1])
        fd_val = qnum * cov_inv[1] - np.dot(np.dot(cov_inv[1], tmat), cov_inv[1]) \
               - np.dot(eff_mat.T, per_kin.dot(eff_mat))
        fd_val[np.tril_indices(cov_dim[1], k=-1)] = 2.0 * fd_val[np.tril_indices(cov_dim[1], k=-1)]
        fd_mat.extend(list(-0.5 * fd_val[np.tril_indices(cov_dim[1], k=0)]))
        # error part
        fd_val = -0.5 * (num_record / var_com[-1] - np.sum((wmat.T.dot(wmat)).multiply(cmat)) \
                       / (var_com[-1] * var_com[-1]) - np.sum(np.dot(e.T, e) / (var_com[-1] * var_com[-1])))
        fd_mat.append(fd_val)
        return np.array(fd_mat)

    def cal_ai_mat():
        """
        Calculate the AI matrix.
        """
        wv = []
        for i in range(len(cov_dim)):
            dial = sparse.eye(zmat_con_lst[i].shape[1] / cov_dim[i], dtype=np.float64)
            for j in range(cov_dim[i]):
                for k in range(j + 1):
                    var_fd = np.zeros((cov_dim[i], cov_dim[i]))  # Notice
                    var_fd[j, k] = var_fd[k, j] = 1.0
                    temp = sparse.kron(np.dot(var_fd, cov_inv[i]), dial)
                    temp = temp.dot(eff[eff_ind[i + 1][0]:eff_ind[i + 1][-1], :])
                    temp = zmat_con_lst[i].dot(temp)
                    wv.append(temp)
        wv.append(e / var_com[-1])
        qmat = np.concatenate(wv, axis=1)
        qrq = np.divide(np.dot(qmat.T, qmat), var_com[-1])
        left = np.divide(wmat.T.dot(qmat), var_com[-1])
        eff_qmat = np.dot(cmat, left)
        ai_mat = np.subtract(qrq, np.dot(left.T, eff_qmat))
        ai_mat = 0.5 * ai_mat
        return ai_mat

    def cal_em_mat():
        """
        Calculate the em matrix.
        """
        num_var_com = len(var_com)
        em_mat = np.zeros((num_var_com, num_var_com))
        b = 0
        cov_mat = []
        for i in range(len(cov_dim)):
            ind = np.tril_indices(cov_dim[i])
            temp = np.zeros((len(ind[0]), len(ind[0])))
            q = zmat_con_lst[i].shape[1] / cov_dim[i]
            a = b
            b = b + len(ind[0])
            covar = np.zeros((cov_dim[i], cov_dim[i]))
            covar[ind] = var_com[a:b]
            covar = np.add(covar, np.tril(covar, -1).T)
            cov_mat.append(covar)
            for j in range(len(ind[0])):
                for k in range(j + 1):
                    temp[j, k] = (cov_mat[i][ind[0][j], ind[0][k]] * cov_mat[i][ind[1][j], ind[1][k]] + \
                                  cov_mat[i][ind[0][j], ind[1][k]] * cov_mat[i][ind[1][j], ind[0][k]]) / (2.0 * q)
            em_mat[a:b, a:b] = temp.copy()
        em_mat[-1, -1] = (var_com[-1] * var_com[-1]) / num_record
        em_mat = 2.0 * em_mat
        em_mat += np.tril(em_mat, k=-1).T
        return linalg.inv(em_mat)

    while iter_count < maxiter:
        iter_count += 1
        logging.info('***Start the iteration: ' + str(iter_count) + ' ***')
        logging.info("Prepare the coefficient matrix")
        cmat = (cmat_pure.multiply(1.0 / var_com[-1])).toarray()
        cmat = cal_cmat_inv(cmat)
        rhs_mat = np.divide(rhs_pure, var_com[-1])
        eff = np.dot(cmat, rhs_mat)
        e = y - np.dot(xmat, eff[:eff_ind[0][1], :]) - zmat_con.dot(
            eff[eff_ind[0][1]:, :])
        logging.info("first-order derivative")
        fd_mat = cal_fd_mat(cmat)
        np.savetxt(out_file + '.fd', fd_mat)
        logging.info("AI matrix")
        ai_mat = cal_ai_mat()
        np.savetxt(out_file + '.ai', ai_mat)
        logging.info("EM matrix")
        em_mat = cal_em_mat()
        np.savetxt(out_file + '.em', em_mat)
        # Increase em weight to guarantee variances positive
        gamma = -em_weight_step
        while gamma < 1.0:
            gamma = gamma + em_weight_step
            if gamma >= 1.0:
                gamma = 1.0
            wemai_mat = (1 - gamma) * ai_mat + gamma * em_mat
            delta = np.dot(linalg.inv(wemai_mat), fd_mat)
            var_com_update = var_com + delta
            var_df['var_com'] = var_com_update
            cov_inv = pre_cov_inv(cov_dim, var_com_update)
            if cov_inv is not None:
                logging.info('EM weight value: ' + str(gamma))
                break
        var_df.to_csv(out_file + '.var', sep='\t', index=False)
        if cov_inv is None:
            logging.error("ERROR: Updated variances is not positive define!")
            sys.exit()
        # Convergence criteria
        cc_par_val = np.sum(pow(delta, 2)) / np.sum(pow(var_com_update, 2))
        cc_par_val = np.sqrt(cc_par_val)
        cc_gra_val = np.sqrt(np.sum(pow(fd_mat, 2))) / len(var_com)
        var_com = var_com_update.copy()
        logging.info("Change in parameters: {}, Norm of gradient vector: {}".format(cc_par_val, cc_gra_val))
        if cc_par_val < cc_par and cc_gra_val < cc_gra:
            break
    if cc_par_val < cc_par and cc_gra_val < cc_gra:
        logging.info("Variances Converged")
    else:
        logging.info("Variances not Converged")
    var_df['var_com'] = var_com
    return var_df
