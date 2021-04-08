from snakewrap.__version__ import *
from sys import version_info

def test_more_info():
    get_more_info()
    assert isinstance(BRANCH, str) is True


def test_mod_string():
    test_str = "test_str"
    if (version_info >= (3,0)):
        test_str = b"test_str"
    assert (mod_string(test_str) == "test_str") is True
