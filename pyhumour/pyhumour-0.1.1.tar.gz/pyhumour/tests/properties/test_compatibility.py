"""Unit tests for _properties/compatibility.py."""

# pylint: disable=protected-access
# pylint: disable=invalid-name,missing-docstring

import unittest
from unittest import mock

from pyhumour._properties.compatibility import Compatibility


class TestCompatibility(unittest.TestCase):
    def test_calculate(self):
        text = "sample text"
        compatibility = Compatibility()
        with \
            mock.patch(
                'pyhumour._properties.compatibility.word_tokenize',
                return_value=['sample', 'text']):
            result = compatibility.calculate(text=text)
        self.assertEqual(result, 4.0)
