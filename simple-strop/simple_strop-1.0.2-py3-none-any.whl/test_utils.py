from . import utils


def test_is_capitalized():
    test_value_pairs = [
        ("a", False),
        ("z", False),
        ("A", True),
        ("Z", True),
        (".", True),
        ("Test", True),
        ("test", False),
    ]

    for tst, res in test_value_pairs:
        assert utils.is_capitalized(tst) == res


def test_is_all_caps():
    test_value_pairs = [
        ("aaaaa", False),
        ("AaaaA", False),
        ("AAAAAAAAA", True),
        ("A", True),
        ("a", False),
        ("aaAaaa", False),
        (".....", True),
        ("AAAA!", True),
        ("...aa.", False),
    ]

    for tst, res in test_value_pairs:
        assert utils.is_all_caps(tst) == res


def test_is_vowel():
    test_value_pairs = [
        (".", False),
        ("a", True),
        ("e", True),
        ("i", True),
        ("o", True),
        ("u", True),
        ("d", False),
        ("y", False),
        ("A", True),
        ("$", False),
    ]

    for tst, res in test_value_pairs:
        assert utils.is_vowel(tst) == res


def test_is_consonant():
    test_value_pairs = [
        (".", False),
        ("a", False),
        ("e", False),
        ("i", False),
        ("o", False),
        ("u", False),
        ("d", True),
        ("y", True),
        ("A", False),
        ("$", False),
    ]

    for tst, res in test_value_pairs:
        assert utils.is_consonant(tst) == res
