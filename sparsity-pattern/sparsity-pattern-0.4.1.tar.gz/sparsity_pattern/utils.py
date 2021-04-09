import math
from typing import List, Dict
from .generators import circledet


def get_matrix_dims_circle(n_max_params: int,
                           info: bool = False) -> List[Dict]:
    """Determine the matrix dimension of quadratic sparse matrix with
    the 'circle' pattern for a given maximum number matrix elements.

    Args:
        n_max_params (int): The desired number of matrix elements.
        info (boo, optional): Request additional information.

    Returns:
        List[Dict]: All combinations of matrix dimensions `n` and `offsets`
            that can squeeze as many as possible weights/elements into the
            sparse matrix.

                [..., {'n': 10, 'offsets': [1, 2, 3]}, ...]

    Examples:
        import sparsity_pattern as spat
        n_max_params = 50
        hyperparams = spat.utils.get_matrix_dims_circle(n_max_params)
        A = spat.get("circle", **hyperparams[0])
        B = spat.get("circle", **hyperparams[1])
        ...

    """
    all_combo = []
    # The square root `int(sqr(n_max_params))` is the first smallest matrix
    # dimension `n_min_dim` that can hold most of the desired `n_max_params`
    # of weights. However, we need to subtract `-1` because the diagonals
    # are assumed to be 0. `n_min_dim` is also the the maximum number of
    # offsets we can squeeze into such a matrix.
    n_min_dim = int(math.sqrt(n_max_params)) - 1

    # loop over `n_offsets = [1, 2, .. n_min_dim]`
    for n_offsets in range(1, n_min_dim + 1):
        # compute matrix dimension. How many offsets can be created for the
        # given number of parameters
        n_dim = n_max_params // n_offsets

        # save results
        result = {"n": n_dim, "offsets": list(range(1, n_offsets + 1))}

        # add more information
        if info:
            pat = circledet(n_dim, range(1, n_offsets + 1))
            n_act_params = len(pat)
            result = {**result, "n_act_params": n_act_params,
                      "ratio_squeezed": n_act_params / n_max_params}

        # save to list
        all_combo.append(result)

    return all_combo
