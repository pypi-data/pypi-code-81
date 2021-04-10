import pytest

from project_tooling_commons.base import stripAccents, isBase64

__author__ = "Juan David"
__copyright__ = "Juan David"
__license__ = "MIT"


def test_stripAccents():
    """API Tests"""
    assert stripAccents("Camión") == "Camion"
    assert stripAccents("Andalucía") == "Andalucía"
    assert stripAccents("Córdoba") == "Córdoba"
    assert stripAccents("Niño") == "Nino"
    with pytest.raises(AssertionError):
        stripAccents(None)


def test_isbase64():
    """isBase64 Test"""
    assert isBase64(b'SG9sYU11bmRv')
    assert isBase64(b'MiCadena') == False
