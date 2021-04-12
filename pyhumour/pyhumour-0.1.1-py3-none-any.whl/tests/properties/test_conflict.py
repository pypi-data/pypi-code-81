from unittest import TestCase, main
from pyhumour._properties.conflict import Conflict
from collections import defaultdict


class MockPosTagBigramFrequencyMatrix:
    def __init__(self):
        placeholder_dict = {('bad', 'fool'): 10, ('generous', 'woman'): 20, ('peculiar', 'sight'): 35}
        self.sample_pairs_frequencies = defaultdict(int)
        for key, value in placeholder_dict.items():
            self.sample_pairs_frequencies[key] = value

    def cell_value(self, adjective, noun):
        return self.sample_pairs_frequencies[(adjective, noun)]


class ConflictTests(TestCase):
    def setUp(self) -> None:
        self.mock_frequency_matrix = MockPosTagBigramFrequencyMatrix()
        self.conflict_calculator = Conflict(self.mock_frequency_matrix)

    def test_empty(self):
        pos_tags = []
        self.assertEqual(self.conflict_calculator.calculate(pos_tags), 0)
        pos_tags = [('she', 'PRP'), ('is', 'VBZ')]
        self.assertEqual(self.conflict_calculator.calculate(pos_tags), 0)

    def test_sentence_1(self):
        pos_tags = [('she', 'PRP'), ('is', 'VBZ'), ('a', 'DT'), ('bad', 'JJ'), ('fool', 'NN')]
        self.assertEqual(self.conflict_calculator.calculate(pos_tags), self.mock_frequency_matrix.cell_value('bad', 'fool'))

    def test_sentence_2(self):
        pos_tags = [('Her', 'PRP$'), ('being', 'VBG'), ('a', 'DT'),
                    ('generous', 'JJ'), ('woman', 'NN'), ('is', 'VBZ'),
                    ('quite', 'RB'), ('a', 'DT'), ('peculiar', 'JJ'), ('sight', 'NN')]
        self.assertEqual(self.conflict_calculator.calculate(pos_tags), 27.5)
