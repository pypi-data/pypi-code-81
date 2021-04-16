from refinitiv.dataplatform.tools._common import is_int


def test_is_int():
    assert is_int("1") is True
    assert is_int(1) is True

    assert is_int({}) is False
    assert is_int(None) is False
    assert is_int("1asb") is False
