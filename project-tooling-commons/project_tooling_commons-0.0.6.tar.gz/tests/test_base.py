from typing import TypeVar
import pytest

from project_tooling_commons.base import strip_accents, is_base64

__author__ = "Juan David"
__copyright__ = "Juan David"
__license__ = "MIT"


def test_strip_accents():
    """API Tests"""
    assert strip_accents("Camión") == "Camion"
    assert strip_accents("Andalucía") == "Andalucia"
    assert strip_accents("Córdoba") == "Cordoba"
    assert strip_accents("Niño") == "Nino"
    with pytest.raises(TypeError):
        strip_accents(None)


def test_is_base64():
    """isBase64 Test"""
    assert is_base64(b'SG9sYU11bmRv')
    assert is_base64('SG9sYU11bmRv')
    assert is_base64(b'MiCadena') == False
