import numpy as np

def check_not_2D(X):
    """
    X: ndarray
    """
    if len(X.shape) == 2:
        return False
    else:
        return True
def check_is_1D(X):
    """
    X: ndarray
    """
    if len(X.shape) == 1:
        return True
    else:
        return False