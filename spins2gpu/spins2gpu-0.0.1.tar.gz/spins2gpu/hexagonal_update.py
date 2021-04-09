#!/usr/bin/env python3

from spins import hexagonal_update_ij

def update(lattices_0, lattices_1, lattices_2, lattices_3, Ja, randval, rnu, val, rank, blocks, threads):

    # Update 0
    rnu.Uniform(randval)
    hexagonal_update_ij.update[blocks, threads](lattices_0[rank], lattices_3[rank], lattices_1[rank], lattices_2[rank], Ja, randval, 0, val)
    # Update 1
    rnu.Uniform(randval)
    hexagonal_update_ij.update[blocks, threads](lattices_1[rank], lattices_2[rank], lattices_0[rank], lattices_3[rank], Ja, randval, 1, val)
    # Update 2
    rnu.Uniform(randval)
    hexagonal_update_ij.update[blocks, threads](lattices_2[rank], lattices_1[rank], lattices_3[rank], lattices_0[rank], Ja, randval, 2, val)
    # Update 3
    rnu.Uniform(randval)
    hexagonal_update_ij.update[blocks, threads](lattices_3[rank], lattices_0[rank], lattices_2[rank], lattices_1[rank], Ja, randval, 3, val)