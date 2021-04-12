from unittest import TestCase, main
from pyhumour._properties.adjective_absurdity import AdjectiveAbsurdity
from collections import defaultdict


class MockPosTagBigramFrequencyMatrix:
    def __init__(self):
        placeholder_dict = {('bad', 'fool'): 10, ('generous', 'woman'): 20, ('peculiar', 'sight'): 35,
                            ('generous', 'fool'): 20, ('peculiar', 'fool'): 40, ('common', 'fool'): 60}

        self.sample_pairs_frequencies = defaultdict(int)
        for key, value in placeholder_dict.items():
            self.sample_pairs_frequencies[key] = value

        self.column_keys = {'fool', 'woman', 'sight'}
        self.column = defaultdict(set)
        self.columns = {'fool': {'bad', 'generous', 'peculiar', 'common'},
                        'woman': {'generous'},
                        'sight': {'peculiar'}}

        self.sample_pairs_frequencies = defaultdict(int)
        for key, value in placeholder_dict.items():
            self.sample_pairs_frequencies[key] = value

    def get_column(self, word: str) -> set:
        return self.columns[word]

    def get_all_column_keys(self) -> set:
        return self.column_keys

    def cell_value(self, adjective, noun):
        return self.sample_pairs_frequencies[(adjective, noun)]


class AdjectiveAbsurdityTests(TestCase):
    def setUp(self) -> None:
        self.mock_frequency_matrix = MockPosTagBigramFrequencyMatrix()
        self.adjective_absurdity_calculator = AdjectiveAbsurdity(self.mock_frequency_matrix)

    # done
    def test_empty(self):
        pos_tags = []
        self.assertEqual(self.adjective_absurdity_calculator.calculate(pos_tags), 0)
        pos_tags = [('she', 'PRP'), ('is', 'VBZ')]
        self.assertEqual(self.adjective_absurdity_calculator.calculate(pos_tags), 0)

    def test_sentence_1(self):
        pos_tags = [('she', 'PRP'), ('is', 'VBZ'), ('a', 'DT'), ('bad', 'JJ'), ('fool', 'NN')]
        self.assertEqual(self.adjective_absurdity_calculator.calculate(pos_tags), 0.07692307692307693)

    def test_sentence_2(self):
        pos_tags = [('Her', 'PRP$'), ('being', 'VBG'), ('a', 'DT'),
                    ('generous', 'JJ'), ('woman', 'NN'), ('is', 'VBZ'),
                    ('quite', 'RB'), ('a', 'DT'), ('peculiar', 'JJ'), ('sight', 'NN')]
        self.assertEqual(self.adjective_absurdity_calculator.calculate(pos_tags), 1.0)
