#!/usr/bin/env python3

import math
from numba import cuda

@cuda.jit
def update(lattice_0, lattice_1, lattice_2, lattice_3, Ja, randval, color, val):
    n, m = lattice_0.shape
    tid = cuda.blockIdx.x * cuda.blockDim.x + cuda.threadIdx.x
    i = tid // m
    j = tid % m

    if (i >= n or j >= m): return

    # Set stencil indices with periodicity
    ipp = (i + 1) if (i + 1) < n else 0
    jpp = (j + 1) if (j + 1) < m else 0
    inn = (i - 1) if (i - 1) >= 0 else (n - 1)
    jnn = (j - 1) if (j - 1) >= 0 else (m - 1)

    # Compute sum of nearest neighbor spins
    if color == 0:
        nn_sum = Ja * ( lattice_1[i, j] + lattice_1[i, jpp] + lattice_2[inn, j] + lattice_2[i, j] + lattice_3[inn, jpp] + lattice_3[i, j] )
    elif color == 1:
        nn_sum = Ja * ( lattice_1[i, j] + lattice_1[i, jpp] + lattice_2[i, j] + lattice_2[ipp, j] + lattice_3[i, jpp] + lattice_3[ipp, j] )
    elif color == 2:
        nn_sum = Ja * ( lattice_1[i, jnn] + lattice_1[i, j] + lattice_2[i, j] + lattice_2[ipp, j] + lattice_3[i, j] + lattice_3[ipp, jnn] )
    elif color == 3:
        nn_sum = Ja * ( lattice_1[i, jnn] + lattice_1[i, j] + lattice_2[inn, j] + lattice_2[i, j] + lattice_3[inn, j] + lattice_3[i, jnn] )

    # Determine whether to flip spin
    lij = lattice_0[i, j]
    acceptance_ratio = math.exp(-2.0 * val * nn_sum * lij)
    if (randval[i, j] < acceptance_ratio):
        lattice_0[i, j] = -lij
