import scipy.sparse
import numpy as np
import itertools
from typing import List, Optional, Union
Number = Union[bool, int, float]


def idseqs_to_mask(idseqs: List[List[int]],
                   n_seqlen: Optional[int] = None,
                   n_vocab_sz: Optional[int] = None,
                   ignore: Optional[List[int]] = [],
                   dtype: Optional[np.dtype] = np.bool_,
                   dense: Optional[bool] = False
                   ) -> List[scipy.sparse.csc_matrix]:
    """Convert ID sequences into mask matrices

    Parameter:
    ----------
    idseqs: List[List[int]]
        A list of ID sequences. Each ID basically a row-index.
          It's assumed that sequences are already padded!

    n_seqlen: Optional[int] = None
        The expected sequence length.

    n_vocab_sz: Optional[int] = None
        The number distinct IDs of all sequences.

    ignore: Optional[List[int]] = []
        A list of IDs to ignore, e.g. ignore=[VOCAB.index("[PAD]")]
          As a result the empty rows of the mask matrix are removed
          accordingly.

    dtype: Optional[np.dtype] = bool
        Data type of the mask matrix, e.g. np.bool_ (True/False),
          np.int8 (0/1), np.float32 (0.0/1.0)

    dense: Optional[bool] = False
        Flag to return a dense mask matrix

    Returns:
    --------
    List[scipy.sparse.csc_matrix]
        A list of CSC matrices (Compressed Sparse Column matrices) which
          perform better when reading column by column (e.g. token by token).
          The CSC matrices are mask matrices.

    Example:
    --------
        idseqs = [[1,2,3,4,0,0,1,2], [2,4,2,0,1]]
        masks = idseqs_to_mask(idseqs, n_seqlen=4, ignore=[3], dense=True)
        # Only for "dense" => <batch_sz, n_seqlen, n_feats>
        masks = np.stack(masks)

    Help:
    -----
    - dtype: https://numpy.org/devdocs/user/basics.types.html
    """
    if n_seqlen is None:
        n_seqlen = max([len(seq) for seq in idseqs])

    # create a list of IDs
    if n_vocab_sz is None:
        ids = set(itertools.chain(*idseqs))
    else:
        ids = set(range(0, n_vocab_sz))

    # remove IDs that we ignore
    ids = ids.difference(set(ignore))
    n_rows = len(ids)

    # convert to list to lookup with .index() method
    ids = list(ids)

    # loop over each ID sequence
    masks = []
    for seq in idseqs:
        # extract index pairs of the sparse matrix
        rowidx = []
        colidx = []
        for col, elem in enumerate(seq[:n_seqlen]):
            try:
                rowidx.append(ids.index(elem))
                colidx.append(col)
            except Exception:
                pass
        # convert to CSC sparse matrix
        tmp = scipy.sparse.csc_matrix(
            ([1 for _ in range(len(rowidx))], (rowidx, colidx)),
            shape=(n_rows, n_seqlen), dtype=dtype)
        # convert to dense matrix if requested
        if dense:
            tmp = tmp.toarray()
        # save it
        masks.append(tmp)

    # done
    return masks
