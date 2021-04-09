from itertools import combinations
from typing import List


def get(sp: str, *args, **kwargs) -> List[List[int]]:
    """Wrapper function for sparsity patterns

    Args:
        sp (str): type of sparsity pattern, e.g.,
            - 'diag' -- Diagonal matrix
            - 'dense' -- Dense matrix
            - 'nodiag' -- Dense without main diagonal elements
            - 'block' -- Block matrix
            - 'circle' -- Circular shift the main diagonal
            - 'tril' -- Lower triangle matrix
            - 'triu' -- Upper triangle matrix
        args: depends on sp
        kwargs: depends on sp

    Returns:
        List[List[int]]: Sparsity pattern as list of row/column-pairs
            or -keys (dictionary of keys format)

    Example:
        idx = sparsity_pattern.get('diag', n=5)
        idx = sparsity_pattern.get('dense', n=5)
        idx = sparsity_pattern.get('dense', r=3, c=5)
        idx = sparsity_pattern.get('nodiag', n=5)
        idx = sparsity_pattern.get('nodiag', r=3, c=5)
        idx = sparsity_pattern.get('block', n=5, block_sizes=2)
        idx = sparsity_pattern.get('block', n=5, block_sizes=[2, 3])
        idx = sparsity_pattern.get('circle', n=5, offsets=1)
        idx = sparsity_pattern.get('circle', n=5, offsets=[1, 2])
        idx = sparsity_pattern.get('tril', n=5, k=-1)
        idx = sparsity_pattern.get('triu', n=5, k=-1)
    """
    if sp in ("diag"):
        arr = diag(*args, **kwargs)
    elif sp in ("dense"):
        if (len(args) + len(kwargs)) == 1:
            arr = dense_quadratic(*args, **kwargs)
        else:
            arr = dense_pythonic(*args, **kwargs)
    elif sp in ("nodiag"):
        if (len(args) + len(kwargs)) == 1:
            arr = nodiag_quadratic(*args, **kwargs)
        else:
            arr = nodiag_pythonic(*args, **kwargs)
    elif sp in ("block"):
        arr = blockflex(*args, **kwargs)
    elif sp in ("circle"):
        arr = circledet(*args, **kwargs)
    elif sp in ("tril"):
        arr = tril(*args, **kwargs)
    elif sp in ("triu"):
        arr = triu(*args, **kwargs)
    # remove duplicates
    arr = list(set(arr))
    # sort by row, col indices
    arr.sort(key=lambda x: (x[0], x[1]))
    return arr


def diag(n: int) -> List[List[int]]:
    """Diagonal Matrix

    Args:
        n (int): Dimension of the quadratic matrix

    Returns:
        List[List[int]]: Sparsity pattern as list of row/column-pairs
            or -keys (dictionary of keys format)
    """
    arr = [(i, i) for i in range(n)]
    return arr


def dense_quadratic(n: int) -> List[List[int]]:
    """A Dense matrix. Quadratic"""
    arr1 = list(combinations(range(n), 2))  # all combinations (only triag)
    arr2 = [(j, i) for i, j in arr1]  # copy flipped indices
    arr3 = [(i, i) for i in range(n)]
    return arr1 + arr2 + arr3


def dense_pythonic(r: int, c: int = None) -> List[List[int]]:
    """A Dense matrix"""
    if c is None:
        c = r
    arr = [(i, j) for j in range(c) for i in range(r)]
    return arr


def nodiag_quadratic(n: int) -> List[List[int]]:
    """Almost Dense matrix without diagonal elements. Quadratic"""
    arr1 = list(combinations(range(n), 2))  # all combinations (only triag)
    arr2 = [(j, i) for i, j in arr1]  # copy flipped indices
    return arr1 + arr2


def nodiag_pythonic(r: int, c: int = None) -> List[List[int]]:
    """Almost Dense matrix without diagonal elements"""
    if c is None:
        c = r
    arr = [(i, j) for j in range(c) for i in range(r) if i != j]
    return arr


def blockflex(n: int, block_sizes=List[int]) -> List[List[int]]:
    """Block Diagonal Matrix with different sized blocks

    Args:
        n (int): Dimension of quadratic matrix
        block_sizes (List[int], int): The block size. Different
            block sizes as list possible that will be repeated,
            e.g., `block_sizes=[2,3]`

    Returns:
        List[List[int]]: Sparsity pattern as list of row/column-pairs
            or -keys (dictionary of keys format)
    """
    if isinstance(block_sizes, int):
        block_sizes = [block_sizes]
    arr = []
    flag = True
    i = 0
    n_blocks = len(block_sizes)
    idx_block_end = 0
    # loop over blocks
    while flag:
        # get the start index of the next block
        h = i % n_blocks
        idx_block_start = idx_block_end
        idx_block_end = min(n, idx_block_start + block_sizes[h])
        indices = range(idx_block_start, idx_block_end)
        # enumerate all index pairs
        arr.extend([(j, k) for k in indices for j in indices])
        # set flag to false
        if idx_block_end >= n:
            flag = False
        i += 1
    return arr


def circledet(n: int, offsets: List[int] = [1]) -> List[List[int]]:
    """Circular shift the main diagonal left/right (or up/down) by an offset

    Args:
        n (int): Dimension of quadratic matrix
        offsets (List[int], default=[1]): Offset to shift a main diagonal
            left/right (up/down).

    Returns:
        List[List[int]]: Sparsity pattern as list of row/column-pairs
            or -keys (dictionary of keys format)
    """
    if isinstance(offsets, int):
        offsets = [offsets]
    arr = []
    off = set(offsets)
    off = [k for k in off if k < n]
    for k in off:
        arr.extend(
            [(i, (i - k) if (i - k) >= 0 else (n + i - k)) for i in range(n)])
    return arr


def tril(n: int, k: int = 0) -> List[List[int]]:
    """Lower triangle matrix

    Args:
        n (int): Dimension of quadratic matrix
        k (int, default=0): All elements exists below the main diagonal (k<0)
            or above the main diagonal (k>0). For k=0 the main diagonal
            elements are 1s.

    Returns:
        List[List[int]]: Sparsity pattern as list of row/column-pairs
            or -keys (dictionary of keys format)
    """
    return [(i, j) for j in range(n) for i in range(max(0, j - k), n)]


def triu(n: int, k: int = 0) -> List[List[int]]:
    """Upper triangle matrix

    Args:
        n (int): Dimension of quadratic matrix
        k (int, default=0): All elements exist above the main diagonal (k<0)
            or below the main diagonal (k>0). For k=0 the main diagonal
            elements are 1s.

    Returns:
        List[List[int]]: Sparsity pattern as list of row/column-pairs
            or -keys (dictionary of keys format)
    """
    return [(i, j) for i in range(n) for j in range(max(0, i - k), n)]
