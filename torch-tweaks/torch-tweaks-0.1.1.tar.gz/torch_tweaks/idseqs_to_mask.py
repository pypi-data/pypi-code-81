import torch.sparse
import itertools
from typing import List, Optional, Union
Number = Union[bool, int, float]


def idseqs_to_mask(idseqs: List[List[int]],
                   n_seqlen: Optional[int] = None,
                   n_vocab_sz: Optional[int] = None,
                   ignore: Optional[List[int]] = [],
                   dtype: Optional[torch.dtype] = torch.bool,
                   dense: Optional[bool] = False
                   ) -> torch.sparse.FloatTensor:
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

    dtype: Optional[torch.dtype] = bool
        Only if dense=True, the data type of the mask matrix,
          e.g. torch.bool (True/False), torch.uint8 (0/1)

    dense: Optional[bool] = False
        Flag to return a dense mask matrix

    Returns:
    --------
    torch.sparse.FloatTensor
        A batch-first FloatTensor <batch_sz, n_seqlen, vocab_sz>

    Example:
    --------
        from torch_tweaks import idseqs_to_mask
        idseqs = [[1,2,3,4,0,0,1,2], [2,4,2,0,1]]
        masks = idseqs_to_mask(idseqs, n_seqlen=5, ignore=[3], dense=True)

    Help:
    -----
    - Sparse module: https://pytorch.org/docs/stable/sparse.html
    - dtype: https://pytorch.org/docs/stable/tensors.html
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
    n_features = len(ids)

    # convert to list to lookup with .index() method
    ids = list(ids)

    # loop over each ID sequence
    masks = []
    for seq in idseqs:
        # extract index pairs of the sparse matrix
        featidx = []
        seqidx = []
        for step, elem in enumerate(seq[:n_seqlen]):
            try:
                featidx.append(ids.index(elem))
                seqidx.append(step)
            except Exception:
                pass
        # convert to COO matrix
        tmp = torch.sparse.FloatTensor(
            indices=torch.LongTensor([seqidx, featidx]),
            values=torch.FloatTensor([1.0 for _ in range(len(seqidx))]),
            size=torch.Size([n_seqlen, n_features])
        ).coalesce()
        # save it
        masks.append(tmp)

    # stack into one 3D tensor <batch_sz, n_seqlen, vocab_sz>
    masks = torch.stack(masks).coalesce()

    # convert to dense matrix if requested
    if dense:
        masks = masks.to_dense().type(dtype)

    # done
    return masks
