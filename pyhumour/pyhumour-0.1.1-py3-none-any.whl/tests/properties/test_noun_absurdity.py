"""Unit tests for _properties/noun_absurdity.py."""

# pylint: disable=protected-access
# pylint: disable=invalid-name,missing-docstring

from collections import defaultdict
from functools import partial
import numpy as np
from unittest import TestCase, mock

from pyhumour._properties.noun_absurdity import NounAbsurdity


class MockPosTagBigramFrequencyMatrix:
    def __init__(self):
        placeholder_dict = {('bad', 'fool'): 10, ('generous', 'woman'): 20, ('peculiar', 'sight'): 35,
                            ('generous', 'fool'): 20, ('peculiar', 'fool'): 40, ('common', 'fool'): 60}

        self.sample_pairs_frequencies = defaultdict(int)
        for key, value in placeholder_dict.items():
            self.sample_pairs_frequencies[key] = value

        self.row_keys = {'bad', 'generous', 'peculiar', 'common'}
        self.row = defaultdict(set)
        self.rows = {'bad': {'fool'},
                     'generous': {'woman', 'fool'},
                     'peculiar': {'sight', 'fool'},
                     'common': {'fool'}}

        self.sample_pairs_frequencies = defaultdict(int)
        for key, value in placeholder_dict.items():
            self.sample_pairs_frequencies[key] = value

    def get_row(self, word: str) -> set:
        return self.rows[word]

    def cell_value(self, adjective, noun):
        return self.sample_pairs_frequencies[(adjective, noun)]


class TestNounAbsurdity(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mock_frequency_matrix = MockPosTagBigramFrequencyMatrix()

        embeddings_index = defaultdict(partial(np.ndarray, 0))
        # the ndarray values are equal to the first 9 values of the actual
        # ConceptNet Embeddings-Index keys
        embeddings_index['fool'] = np.array(
            [-0.0957, -0.1523, 0.1237, -0.1973, -0.0092, -0.0371, 0.035, -0.0819, -0.1077])
        embeddings_index['woman'] = np.array(
            [0.0027, -0.0737, 0.046, -0.0493, -0.0963, 0.0607, -0.0262, -0.0438, 0.0322])
        embeddings_index['sight'] = np.array(
            [-0.1186, -0.1043, 0.0282, 0.0078, -0.041, -0.121, -0.0223, 0.0711, 0.1598])
        with \
            mock.patch(
                'pyhumour._properties.noun_absurdity.get_embeddings_index',
                return_value=embeddings_index):
            cls.noun_absurdity_calculator = NounAbsurdity(cls.mock_frequency_matrix)

    def test_empty_pos_tags(self):
        pos_tags = []
        noun_absurdity_average = self.noun_absurdity_calculator.calculate(pos_tags)

        self.assertEqual(noun_absurdity_average, 0)

    def test_irrelevant_pos_tags(self):
        pos_tags = [('she', 'PRP'), ('is', 'VBZ')]
        noun_absurdity_average = self.noun_absurdity_calculator.calculate(pos_tags)

        self.assertEqual(noun_absurdity_average, 0)

    def test_sentence_1(self):
        pos_tags = [('she', 'PRP'), ('is', 'VBZ'), ('a', 'DT'), ('bad', 'JJ'), ('fool', 'NN')]
        noun_absurdity_average = self.noun_absurdity_calculator.calculate(pos_tags)

        self.assertEqual(noun_absurdity_average, 0.0)

    def test_sentence_2(self):
        pos_tags = [('Her', 'PRP$'), ('being', 'VBG'), ('a', 'DT'),
                    ('generous', 'JJ'), ('woman', 'NN'), ('is', 'VBZ'),
                    ('quite', 'RB'), ('a', 'DT'), ('peculiar', 'JJ'), ('sight', 'NN')]
        noun_absurdity_average = self.noun_absurdity_calculator.calculate(pos_tags)

        self.assertEqual(round(noun_absurdity_average, 1), 0.4)
