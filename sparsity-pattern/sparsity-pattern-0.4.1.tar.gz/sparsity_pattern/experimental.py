from typing import List


def blockdiag(n: int, block_size: int = 2) -> List[List[int]]:
    """Block diagonal matrix.
    Requires mod(n, block_size)==0. Is a quadratic matrix
    """
    if (n % block_size) != 0:
        raise Exception("n must be a multiple of block_size")
    # prepare variables
    n_blocks = n // block_size
    arr = []
    # loop over blocks
    for i in range(n_blocks):
        # get the start index of the next block
        idx_block_start = i * block_size
        idx_block_end = idx_block_start + block_size
        indices = range(idx_block_start, idx_block_end)
        # enumerate all index pairs
        arr.extend([(j, k) for k in indices for j in indices])
    return arr
