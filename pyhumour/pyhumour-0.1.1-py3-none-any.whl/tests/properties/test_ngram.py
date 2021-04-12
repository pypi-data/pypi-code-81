"""Unit tests for _properties/compatibility.py."""

# pylint: disable=protected-access
# pylint: disable=invalid-name,missing-docstring

import unittest
from unittest import mock
from nltk.corpus import words

from pyhumour._properties.language_models import NgramHelper
import string


class TestNgram(unittest.TestCase):
    def setUp(self) -> None:
        self._ngram = NgramHelper(["this is funny", "so damn funny"])

    def test_score(self):
        result = self._ngram.get_ngram_score("damn funny")
        self.assertEqual(result, -6.437751649736401)

    def test_ngramVocabInstance(self):
        self.assertIsInstance(self._ngram.get_vocab(), type(set()))

    def test_ngramVocabValue(self):
        actual = {'is', 'damn', 'so', 'funny', 'this'}
        self.assertEqual(self._ngram.get_vocab(), actual)

    def test_ngramBigramInstance(self):
        self.assertIsInstance(self._ngram.get_bigrams(), type(dict()))

    def test_ngramBigramValue(self):
        bigram = {('<s>', '<s>'): 2, ('<s>', 'this'): 1, ('this', 'is'): 1, ('is', 'funny'): 1, ('funny', '</s>'): 2,
                  ('</s>', '</s>'): 2, ('<s>', 'so'): 1, ('so', 'damn'): 1, ('damn', 'funny'): 1}
        self.assertEqual(self._ngram.get_bigrams(), bigram)

    def test_ngramTrigramInstance(self):
        self.assertIsInstance(self._ngram.get_trigrams(), type(dict()))

    def test_ngramTrigramValue(self):
        trigram = {('<s>', '<s>', 'this'): 1, ('<s>', 'this', 'is'): 1, ('this', 'is', 'funny'): 1,
                   ('is', 'funny', '</s>'): 1, ('funny', '</s>', '</s>'): 2, ('<s>', '<s>', 'so'): 1,
                   ('<s>', 'so', 'damn'): 1, ('so', 'damn', 'funny'): 1, ('damn', 'funny', '</s>'): 1}
        self.assertEqual(self._ngram.get_trigrams(), trigram)

    def test_ngramGoldenVocab(self):
        actual = words.words()
        actual = [word.lower() for word in actual]
        self.assertEqual(self._ngram.get_golden_vocab(), actual)

    def test_ngramGoldenVocabInstance(self):
        self.assertIsInstance(self._ngram.get_golden_vocab(), list)

    def test_ngramUnknownInstanceFalse(self):
        self.assertIsInstance(self._ngram.get_unknown(), set)

    def test_ngramSpecialCharacters(self):
        self.assertEqual(self._ngram.get_special_characters(), string.punctuation + "'[@_!#$%^&*()<>?/\|}{~:]'")

    def test_ngramIndividualSentencesFalse(self):
        # should be empty before calling vocab
        self.assertEqual(self._ngram.get_individual_sentences(), [])

    def test_ngramIndividualSentencesTrue(self):
        self._ngram.get_vocab()
        actual = [['<s>', '<s>', 'this', 'is', 'funny', '</s>', '</s>'],
                  ['<s>', '<s>', 'so', 'damn', 'funny', '</s>', '</s>']]

        self.assertEqual(self._ngram.get_individual_sentences(), actual)
