"""Unit tests for _properties/compatibility.py."""

# pylint: disable=protected-access
# pylint: disable=invalid-name,missing-docstring

import unittest
from unittest import mock

from pyhumour._utilities.preprocess import preprocess_text, preprocess_texts


class TestPreprocess(unittest.TestCase):

    def test_preprocess(self):
        result = preprocess_text("hello world! How's this as a sample sentence.")
        actual = "hello world ! how is this as a sample sentence ."
        self.assertEqual(result,actual)

    def test_preprocessInstance(self):
        self.assertIsInstance(type(preprocess_text("hello")),type(str))

    def test_preprocessTextsInstance(self):
        self.assertIsInstance(type(preprocess_texts(["hello","world"])),type(list))
