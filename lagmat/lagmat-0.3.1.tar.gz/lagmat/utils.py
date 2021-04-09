import numpy as np
import warnings


def chopnan(X: np.array, lags: list = [], nchop: int = None) -> np.array:
    if lags:
        nchop = max(lags)
    if nchop is None:
        raise Exception("No lags=[1,2,..] nor nchop=? has been provided")
    return X[nchop:, :]


def rmnanrow(X: np.array) -> np.array:
    """Remove all rows that contain a NaN value"""
    warnings.warn((
        "This function 'rmnanrow' is for demonstration purpose only. "
        "You may risk to delete rows due to missing values "
        "that need to be fixed during data cleansing before "
        "feature engineering."))
    idx = np.any(np.isnan(X), axis=1)
    return X[np.logical_not(idx), :]
