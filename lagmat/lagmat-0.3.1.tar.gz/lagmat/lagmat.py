import numpy as np


def lagmat(A: np.array, lags: list, orient: str = 'col') -> np.array:
    """Create array with time-lagged copies of the features/variables

    Args:
        A (np.ndarray): Dataset. One column for each features/variables,
            and one row for each example/observation at a certain time step.
        lags (ist, tuple): Definition what time lags the copies of A should
            have.
        orient (str, Default: 'col'): Information if time series in A are in
            column-oriented or row-oriented

    Assumptions:
        - It's a time-homogenous time series (that's why there is
            no time index)
        - Features/Variables are ordered from the oldest example/observation
            (1st row) to the latest example (last row)
        - Any Missing Value treatment have been done previously.
    """
    # detect negative lags
    if min(lags) < 0:
        raise Exception((
            "Negative lags are not allowed. Only provided integers "
            "greater equal 0 as list/tuple elements"))
    # None result for missing lags
    if len(lags) == 0:
        return None
    # enforce floating subtype
    if not np.issubdtype(A.dtype, np.floating):
        A = np.array(A, np.float32)

    if orient in ('row', 'rows'):
        # row-oriented time series
        if len(A.shape) == 1:
            A = A.reshape(1, -1)
        A = np.array(A, order='C')
        return lagmat_rows(A, lags)

    elif orient in ('col', 'cols', 'columns'):
        # column-oriented time series
        if len(A.shape) == 1:
            A = A.reshape(-1, 1)
        A = np.array(A, order='F')
        return lagmat_cols(A, lags)
    else:
        return None


def lagmat_rows(A: np.array, lags: list):
    # number of colums and lags
    n_rows, n_cols = A.shape
    n_lags = len(lags)
    # allocate memory
    B = np.empty(shape=(n_rows * n_lags, n_cols), order='C', dtype=A.dtype)
    B[:] = np.nan
    # Copy lagged columns of A into B
    for i, l in enumerate(lags):
        # target rows of B
        j = i * n_rows
        k = j + n_rows  # (i+1) * n_rows
        # number cols of A
        nc = n_cols - l
        # Copy
        B[j:k, l:] = A[:, :nc]
    return B


def lagmat_cols(A: np.array, lags: list):
    # number of colums and lags
    n_rows, n_cols = A.shape
    n_lags = len(lags)
    # allocate memory
    B = np.empty(shape=(n_rows, n_cols * n_lags), order='F', dtype=A.dtype)
    B[:] = np.nan
    # Copy lagged columns of A into B
    for i, l in enumerate(lags):
        # target columns of B
        j = i * n_cols
        k = j + n_cols  # (i+1) * ncols
        # number rows of A
        nl = n_rows - l
        # Copy
        B[l:, j:k] = A[:nl, :]
    return B
