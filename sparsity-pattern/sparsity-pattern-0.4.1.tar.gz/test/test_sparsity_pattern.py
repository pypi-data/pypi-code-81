import sparsity_pattern


def test1():
    sp = sparsity_pattern.get('diag', 3)
    target = [(0, 0), (1, 1), (2, 2)]
    assert sp == target


def test2():
    sp = sparsity_pattern.get('dense', 2)
    target = [(0, 0), (0, 1), (1, 0), (1, 1)]
    assert sp == target


def test3():
    sp = sparsity_pattern.get('dense', 2, 3)
    target = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    assert sp == target


def test3c():
    sp = sparsity_pattern.get('dense', 2, c=3)
    target = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    assert sp == target


def test3b():
    sp = sparsity_pattern.get('dense', r=2, c=3)
    target = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    assert sp == target


def test4():
    sp = sparsity_pattern.get('nodiag', 3)
    target = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
    assert sp == target


def test5():
    sp = sparsity_pattern.get('nodiag', 2, 3)
    target = [(0, 1), (0, 2), (1, 0), (1, 2)]
    assert sp == target


def test5b():
    sp = sparsity_pattern.get('nodiag', r=2, c=3)
    target = [(0, 1), (0, 2), (1, 0), (1, 2)]
    assert sp == target


def test5c():
    sp = sparsity_pattern.get('nodiag', 2, c=3)
    target = [(0, 1), (0, 2), (1, 0), (1, 2)]
    assert sp == target


def test6():
    sp = sparsity_pattern.get('block', 4, [2])
    target = [(0, 0), (0, 1), (1, 0), (1, 1),
              (2, 2), (2, 3), (3, 2), (3, 3)]
    assert sp == target


def test7a():
    sp = sparsity_pattern.get('block', 3, 2)
    target = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 2)]
    assert sp == target


def test7b():
    sp = sparsity_pattern.get('block', 3, [2, 2])
    target = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 2)]
    assert sp == target


def test8a():
    sp = sparsity_pattern.get('circle', 5, 1)
    target = [(0, 4), (1, 0), (2, 1), (3, 2), (4, 3)]
    assert sp == target


def test8b():
    sp = sparsity_pattern.get('circle', 5, [1, 1])
    target = [(0, 4), (1, 0), (2, 1), (3, 2), (4, 3)]
    assert sp == target


def test9a():
    sp = sparsity_pattern.get('tril', 3, -1)
    target = [(1, 0), (2, 0), (2, 1)]
    assert sp == target


def test9b():
    for n in range(0, 10):
        sp = sparsity_pattern.get('tril', n, -n)
        assert sp == []


def test9c():
    for n in range(0, 10):
        sp = sparsity_pattern.get('tril', n, n)
        sp2 = sparsity_pattern.get('dense', n)
        assert sp == sp2


def test10a():
    sp = sparsity_pattern.get('triu', 3, -1)
    target = [(0, 1), (0, 2), (1, 2)]
    assert sp == target


def test10b():
    for n in range(0, 10):
        sp = sparsity_pattern.get('triu', n, -n)
        assert sp == []


def test10c():
    for n in range(0, 10):
        sp = sparsity_pattern.get('triu', n, n)
        sp2 = sparsity_pattern.get('dense', n)
        assert sp == sp2
