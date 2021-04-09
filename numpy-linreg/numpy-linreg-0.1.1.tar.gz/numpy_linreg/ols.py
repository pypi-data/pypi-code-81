import numpy as np
import numba
import warnings


def lu(y, X):
    """Linear Regression, OLS, by solving linear equations and LU decomposition

    Notes:
        - based on LAPACK's _gesv what applies LU decomposition
        - avoids using python's inverse functions
        - should be stable
        - no overhead or other computations

    Errors:
        Might throw an exception "np.linalg.LinAlgError",
        i.e. X*X' is singular or not square.
    """
    return np.linalg.solve(np.dot(X.T, X), np.dot(X.T, y))


def pinv(y, X, rcond=1e-15):
    """Linear Regression, OLS, by multiplying with Pseudoinverse

    Errors:
        Might throw an exception "np.linalg.LinAlgError",
        i.e. SVD does not converge.
    """
    return np.dot(np.linalg.pinv(np.dot(X.T, X), rcond=rcond), np.dot(X.T, y))


def qr(y, X):
    """Linear Regression, OLS, inverse by QR Factoring

    Errors:
        Might throw an exception "np.linalg.LinAlgError",
        i.e. Factoring failed.
    """
    q, r = np.linalg.qr(np.dot(X.T, X))
    return np.dot(np.dot(np.linalg.inv(r), q.T), np.dot(X.T, y))


def svd(y, X, rcond=1e-15):
    """Linear Regression, OLS, inv by SVD

    Properties:
        - Numpy's lstsq is based on LAPACK's _gelsd what applies SVD
        - SVD inverse might be slow (complex Landau O)
        - speed might decline during forward selection
        - no overhead or other computations

    Errors:
        Might throw an exception "np.linalg.LinAlgError",
        i.e. computation does not converge.
    """
    beta, _, _, singu = np.linalg.lstsq(b=y, a=X, rcond=rcond)

    # check singu
    if np.any(singu < 0.0):
        warnings.warn(
            "Error: A singular value of X is numerically not well-behaved.")
        return None

    # return estimated model parameters
    return beta
