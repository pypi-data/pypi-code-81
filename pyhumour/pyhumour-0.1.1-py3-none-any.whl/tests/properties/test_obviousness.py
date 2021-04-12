"""Unit tests for _properties/obviousness.py."""

# pylint: disable=protected-access
# pylint: disable=invalid-name,missing-docstring

import unittest
from unittest import mock

from pyhumour._properties.obviousness import Obviousness


class TestInappropriateness(unittest.TestCase):
    def test_calculate(self):
        text = "sample text"
        obviousness = Obviousness()
        with \
            mock.patch(
                'pyhumour._properties.inappropriateness.word_tokenize',
                return_value=['sample', 'text']):
            result = obviousness.calculate(text=text)
        self.assertEqual(result, 7.08e-05)
