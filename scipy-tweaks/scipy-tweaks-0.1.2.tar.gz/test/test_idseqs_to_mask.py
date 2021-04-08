from scipy_tweaks import idseqs_to_mask
import scipy.sparse
import numpy.testing as npt


def test1():
    idseqs = [[1, 1, 0, 0, 2, 2, 3], [1, 3, 2, 1, 0, 0, 2]]

    target = [
        scipy.sparse.csc_matrix(
            ([1 for _ in range(6)], ([1, 1, 0, 0, 2, 2], [0, 1, 2, 3, 4, 5])),
            shape=(3, 6), dtype=int),
        scipy.sparse.csc_matrix(
            ([1 for _ in range(5)], ([1, 2, 1, 0, 0], [0, 2, 3, 4, 5])),
            shape=(3, 6), dtype=int)
    ]

    masks = idseqs_to_mask(idseqs, n_seqlen=6, n_vocab_sz=3, ignore=[3],
                           dtype=int, dense=False)

    assert len(masks) == len(target)
    npt.assert_array_equal(masks[0].toarray(), target[0].toarray())
    npt.assert_array_equal(masks[1].toarray(), target[1].toarray())


def test2():
    idseqs = [[1, 1, 0, 0, 2, 2, 3], [1, 3, 2, 1, 0, 0, 2]]

    target = [
        scipy.sparse.csc_matrix(
            ([True for _ in range(6)], ([1, 1, 0, 0, 2, 2],
                                        [0, 1, 2, 3, 4, 5])),
            shape=(3, 6), dtype=bool),
        scipy.sparse.csc_matrix(
            ([True for _ in range(5)], ([1, 2, 1, 0, 0],
                                        [0, 2, 3, 4, 5])),
            shape=(3, 6), dtype=bool)
    ]

    masks = idseqs_to_mask(idseqs, n_seqlen=6, n_vocab_sz=3, ignore=[3],
                           dtype=bool, dense=False)

    assert len(masks) == len(target)
    npt.assert_array_equal(masks[0].toarray(), target[0].toarray())
    npt.assert_array_equal(masks[1].toarray(), target[1].toarray())


def test3():
    idseqs = [[1, 1, 0, 0, 2, 2, 3], [1, 3, 2, 1, 0, 0, 2]]

    target = [
        scipy.sparse.csc_matrix(
            ([1.0 for _ in range(6)], ([1, 1, 0, 0, 2, 2],
                                       [0, 1, 2, 3, 4, 5])),
            shape=(3, 6), dtype=float),
        scipy.sparse.csc_matrix(
            ([1.0 for _ in range(5)], ([1, 2, 1, 0, 0],
                                       [0, 2, 3, 4, 5])),
            shape=(3, 6), dtype=float)
    ]

    masks = idseqs_to_mask(idseqs, n_seqlen=6, n_vocab_sz=3, ignore=[3],
                           dtype=float, dense=False)

    assert len(masks) == len(target)
    npt.assert_array_equal(masks[0].toarray(), target[0].toarray())
    npt.assert_array_equal(masks[1].toarray(), target[1].toarray())


def test4():
    idseqs = [[1, 1, 0, 0, 2, 2, 3], [1, 3, 2, 1, 0, 0, 2]]

    target = [
        scipy.sparse.csc_matrix(
            ([1 for _ in range(4)], ([0, 0, 1, 1], [2, 3, 4, 5])),
            shape=(3, 6), dtype=int),
        scipy.sparse.csc_matrix(
            ([1 for _ in range(4)], ([2, 1, 0, 0], [1, 2, 4, 5])),
            shape=(3, 6), dtype=int)
    ]

    masks = idseqs_to_mask(idseqs, n_seqlen=6, ignore=[1],
                           dtype=int, dense=False)

    assert len(masks) == len(target)
    npt.assert_array_equal(masks[0].toarray(), target[0].toarray())
    npt.assert_array_equal(masks[1].toarray(), target[1].toarray())
