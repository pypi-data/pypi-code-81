'''Utility functions for low rank denoising
Copyright Will Clarke, University of Oxford, 2021'''

import numpy as np


def lsvd(A, r=None, sv_lim=None):
    """Calculate the svd decomposition of A.
    Truncated to rank r or to a SV limit (e.g. determined by MP)
    Copied from Mark Chiew's Matlab code.

    U, S, V = lsvd(A, r)

    U, V are the left and right singular vectors of A
    S contains the singular values

    A is a real or complex input matrix, where size(A,1) > size(A,2)
    r is the desired output rank of U*S*V' where 1 <= r <= size(A,2)

    :param A: Input matrix
    :type A: numpy.ndarray
    :param r: Truncate to rank r, defaults to None (no truncation)
    :type r: int, optional
    :param sv_lim: Singular value threshold, used if r is None.
        Defaults to None
    :type sv_lim: float, optional
    :return: Truncated estimate of A
    :rtype: numpy.ndarray
    """
    # Quick checks
    if r is not None and r < 1:
        raise ValueError('Rank must be > 0')
    if sv_lim is not None and sv_lim < 0.0:
        raise ValueError('sv_lim must be > 0.0')

    if A.shape[1] > A.shape[0]:
        swap = True
        A = A.conj().T
    else:
        swap = False

    D, V = np.linalg.eigh(A.conj().T @ A)
    D[D < 0.0] = 1E-15
    S = D**0.5

    if r is None and sv_lim is None:
        # No truncation
        r = A.shape[1]
    elif r is None and sv_lim > 0.0:
        r = len(S) - np.searchsorted(S, sv_lim)
        if r == 0:
            r = 1
            # raise ValueError('MP limit higher than any singular value.')
        # print(f'Truncate to r = {r}')

    S = S[-r:]
    V = V[:, -r:]
    U = A @ (V @ np.diag(1 / S))
    S = np.diag(S)

    if swap:
        return V, S, U
    else:
        return U, S, V


def svd_trunc(A, r=None, sv_lim=None):
    """SVD based truncation of A to rank r, or SV threshold sv_lim.
    A may have more than 2 dimensions, but it will be
    reshaped to two dimensions, preserving the length of the
    final dimension.

    Also returns estimates of the (unscaled) variance and covariance of the
    truncated matrix A.

    :param A: Input matrix
    :type A: numpy.ndarray
    :param r: Truncate to rank r, defaults to None (no truncation)
    :type r: int, optional
    :param sv_lim: Singular value threshold, used if r is None.
        Defaults to None
    :type sv_lim: float, optional
    :return: Truncated estimate of A
    :rtype: numpy.ndarray
    :return: Estimate of the variance in A
    :rtype: numpy.ndarray
    :return: Estimate of the covariance in the last dimension of A.
    :rtype: numpy.ndarray
    """
    dims = A.shape
    u, s, v = lsvd(A.reshape((-1, dims[-1])), r=r, sv_lim=sv_lim)

    est_var = calc_var(u, v)
    est_covar = calc_covar(v)

    return (u @ s @ v.conj().T).reshape(dims), est_var.reshape(dims), est_covar


def calc_var(u, v):
    """Calculate the unscaled variance from a truncated SVD.
    Uses the method proposed in Chen Y, Fan J, Ma C, Yan Y.
    Inference and uncertainty quantification for noisy matrix completion.
    PNAS 2019;116:22931–22937 doi: 10.1073/pnas.1910053116.

    :param u: Left singular vectors of M
    :type u: numpy.ndarray
    :param v: Right singular vectors of M
    :type v: numpy.ndarray
    :return: Estimated element-wise variance of M
    :rtype: numpy.ndarray
    """
    return (np.linalg.norm(u, axis=1)**2)[:, np.newaxis]\
        + np.linalg.norm(v, axis=1)**2


def calc_covar(u):
    """Calculate the estimated unscaled off-diagonal covariance
    from a truncated SVD.

    :param u: Left or right singular vectors of M
    :type u: numpy.ndarray
    :return: Estimated unscaled off-diagonal covariance of M
    :rtype: numpy.ndarray
    """
    return u @ u.conj().T


def max_sv_from_mp(data_var, data_shape):
    """Calculate the upper Marchenko–Pastur limit for a pure noise
    Matrix of defined shape and data variance.

    :param data_var: Noise variance
    :type data_var: float
    :param data_shape: 2-tuple of data dimensions.
    :type data_shape: tuple
    :return: Upper MP singular value limit
    :rtype: float
    """
    # Make sure dimensions agree with utils.lsvd
    # utils.lsvd will always move largest dimension to first dim.
    if data_shape[1] > data_shape[0]:
        data_shape = (data_shape[1], data_shape[0])

    c = data_shape[1] / data_shape[0]
    sv_lim = data_var * (1 + np.sqrt(c))**2
    return (sv_lim * data_shape[0])**0.5
