from d8s_random import (
    random_number,
    random_integer,
    random_xkcd_integer,
    random_dilbert_integer,
    random_shuffle,
    random_choice,
    random_sample,
    random_choices,
)
from d8s_math import permutations


def test_random_choices_docs_1():
    result = random_choices([1, 2, 3, 3], 2)
    assert len(result) == 2
    assert result.count(1) + result.count(2) + result.count(3) == 2


def test_random_number_docs_1():
    r = random_number()
    assert r >= 0 and r < 1


def test_random_integer_docs_1():
    r = random_integer()
    assert r >= 0 and r <= 10

    a = 10
    b = 100
    r = random_integer(a=a, b=b)
    assert r >= a and r <= b


def test_random_xkcd_integer_docs_1():
    assert random_xkcd_integer() == 4


def test_random_dilbert_integer_docs_1():
    assert random_dilbert_integer() == 9


def test_random_shuffle_docs_1():
    r = random_shuffle([1, 2, 3])
    print(r)
    assert len(r) == 3
    assert 1 in r
    assert 2 in r
    assert 3 in r


def test_random_choice_docs_1():
    r = random_choice([1, 2, 3])
    assert r == 1 or r == 2 or r == 3


def test_random_sample_docs_1():
    r = random_sample([1, 2, 3], 2)
    assert len(r) == 2

    combos = permutations([1, 2, 3], length=2)
    r = tuple(r)
    for combo in combos:
        if combo == r:
            break
    else:
        raise AssertionError(f'The result of random_sample ({r}) did not match any of the expected combos ({combos})')
