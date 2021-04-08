from torch_tweaks import idseqs_to_mask
import torch


def test1():
    idseqs = [[1, 1, 0, 0, 2, 2, 3], [1, 3, 2, 1, 0, 0, 2]]

    target = torch.sparse.FloatTensor(
        indices=torch.LongTensor([
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [0, 1, 2, 3, 4, 5, 0, 2, 3, 4, 5],
            [1, 1, 0, 0, 2, 2, 1, 2, 1, 0, 0]]),
        values=torch.FloatTensor([1. for _ in range(11)]),
        size=torch.Size([2, 6, 3])
    ).coalesce()

    masks = idseqs_to_mask(
        idseqs, n_seqlen=6, n_vocab_sz=3, ignore=[3], dense=False)

    assert (masks.to_dense() == target.to_dense()).all()
    assert masks.dtype == target.dtype


def test2():
    idseqs = [[1, 1, 0, 0, 2, 2, 3], [1, 3, 2, 1, 0, 0, 2]]

    target = torch.sparse.FloatTensor(
        indices=torch.LongTensor([
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [0, 1, 2, 3, 4, 5, 0, 2, 3, 4, 5],
            [1, 1, 0, 0, 2, 2, 1, 2, 1, 0, 0]]),
        values=torch.FloatTensor([True for _ in range(11)]),
        size=torch.Size([2, 6, 3])
    ).to_dense().type(torch.bool)

    masks = idseqs_to_mask(
        idseqs, n_seqlen=6, n_vocab_sz=3, ignore=[3],
        dense=True, dtype=torch.bool)

    assert (masks == target).all()
    assert masks.dtype == target.dtype


def test3():
    idseqs = [[1, 1, 0, 0, 2, 2, 3], [1, 3, 2, 1, 0, 0, 2]]

    target = torch.sparse.FloatTensor(
        indices=torch.LongTensor([
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [0, 1, 2, 3, 4, 5, 0, 2, 3, 4, 5],
            [1, 1, 0, 0, 2, 2, 1, 2, 1, 0, 0]]),
        values=torch.FloatTensor([1 for _ in range(11)]),
        size=torch.Size([2, 6, 3])
    ).to_dense().type(torch.uint8)

    masks = idseqs_to_mask(
        idseqs, n_seqlen=6, n_vocab_sz=3, ignore=[3],
        dense=True, dtype=torch.uint8)

    assert (masks == target).all()
    assert masks.dtype == target.dtype


def test4():
    idseqs = [[1, 1, 0, 0, 2, 2, 3], [1, 3, 2, 1, 0, 0, 2]]

    target = torch.sparse.FloatTensor(
        indices=torch.LongTensor([
            [0, 0, 0, 0, 1, 1, 1, 1],
            [2, 3, 4, 5, 1, 2, 4, 5],
            [0, 0, 1, 1, 2, 1, 0, 0]]),
        values=torch.FloatTensor([1. for _ in range(8)]),
        size=torch.Size([2, 6, 3])
    ).coalesce()

    masks = idseqs_to_mask(
        idseqs, n_seqlen=6, ignore=[1], dense=False)

    assert (masks.to_dense() == target.to_dense()).all()
    assert masks.dtype == target.dtype
