"""Unit tests for _properties/inappropriateness.py."""

# pylint: disable=protected-access
# pylint: disable=invalid-name,missing-docstring

import unittest
from unittest import mock

from pyhumour._properties.inappropriateness import Inappropriateness


class TestInappropriateness(unittest.TestCase):
    def test_calculate(self):
        text = "sample text"
        inappropriateness = Inappropriateness()
        with \
            mock.patch(
                'pyhumour._properties.inappropriateness.word_tokenize',
                return_value=['sample', 'text']):
            result = inappropriateness.calculate(text=text)
        self.assertEqual(result, 0.33978718643103556)
