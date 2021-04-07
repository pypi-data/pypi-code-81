import numpy as np


def aggregate_matrices(*args, dtype=np.float64):
    # check inputs
    if len(args) % 2:
        raise Exception("An even number of input arguments expected")

    # copy the first matrix
    out = np.array(args[0], dtype=dtype) * dtype(args[1])

    # add the other matrices
    for i in range(2, len(args), 2):
        out += (np.array(args[i], dtype=dtype) * dtype(args[i + 1]))

    # done
    return out
