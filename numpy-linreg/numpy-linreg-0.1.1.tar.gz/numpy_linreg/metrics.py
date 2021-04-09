import numpy as np
import numba


@numba.jit(nopython=True)
def ssr(y, X, beta):
    return np.sum((y - np.dot(X, beta))**2)


@numba.jit(nopython=True)
def mse(y, X, beta):
    return np.mean((y - np.dot(X, beta))**2)


@numba.jit(nopython=True)
def rmse(y, X, beta):
    return np.sqrt(np.mean((y - np.dot(X, beta))**2))
