import numpy as np
import numba


@numba.jit(nopython=True)
def lu(y, X, lam=0.01):
    """Ridge Regression with LU Decomposition

    Errors:
        Might throw an exception "np.linalg.LinAlgError",
        i.e. X*X'+lam*I is singular or not square.
    """
    n_vars = X.shape[1]
    P = np.dot(X.T, X) + lam * np.eye(n_vars)
    return np.linalg.solve(P, np.dot(X.T, y))
