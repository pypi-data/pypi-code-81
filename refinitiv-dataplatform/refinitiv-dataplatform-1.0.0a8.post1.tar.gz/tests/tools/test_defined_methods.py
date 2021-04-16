from refinitiv.dataplatform.tools._common import is_all_defined, is_any_defined


def test_is_all_defined_true():
    assert is_all_defined([1], [1])
    assert is_all_defined({1}, {1})
    assert is_all_defined({1: 1}, {1: 1})
    assert is_all_defined("1", "1")
    assert is_all_defined(1, 1)
    assert is_all_defined(True, True)


def test_is_all_defined_false():
    assert not is_all_defined([], [1])
    assert not is_all_defined(set(), {1, })
    assert not is_all_defined({}, {1: 1})
    assert not is_all_defined("", "1")
    assert not is_all_defined(0, 1)
    assert not is_all_defined(False, True)


def test_is_any_defined_true():
    assert is_any_defined([1], set(), {},     "",  0, False)
    assert is_any_defined([],  {1},   {},     "",  0, False)
    assert is_any_defined([],  set(), {1: 1}, "",  0, False)
    assert is_any_defined([],  set(), {},     "1", 0, False)
    assert is_any_defined([],  set(), {},     "",  1, False)
    assert is_any_defined([],  set(), {},     "",  0, True)


def test_is_any_defined_false():
    assert not is_any_defined([], set(), {}, "", 0, False)
