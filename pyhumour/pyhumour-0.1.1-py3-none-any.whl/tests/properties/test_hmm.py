"""Unit tests for _properties/compatibility.py."""

# pylint: disable=protected-access
# pylint: disable=invalid-name,missing-docstring

import unittest
from unittest import mock

import keras
import hmmlearn
from pyhumour._properties.language_models import HMMHelper


class TestHMM(unittest.TestCase):
    def setUp(self) -> None:
        self._hmm = HMMHelper(["this is funny","so damn funny"]+["not funny","so not funny"])

    def test_score(self):

        result = self._hmm.get_hmm_score("damn funny")
        self.assertEqual(round(result,3), -7.687)

    def test_tokenizer(self):
        self.assertIsInstance(type(self._hmm.get_tokenizer(123)),type(keras.preprocessing.text.Tokenizer))

    def test_hmmObject(self):
        self.assertIsInstance(type(self._hmm.get_hmm()),type(hmmlearn.hmm.GaussianHMM))
