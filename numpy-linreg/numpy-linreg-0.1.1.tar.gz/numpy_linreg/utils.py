import numpy as np
import numba


@numba.jit(nopython=True)
def predict(X, beta):
    return np.dot(X, beta)


@numba.jit(nopython=True)
def residuals(y, X, beta):
    return y - np.dot(X, beta)
