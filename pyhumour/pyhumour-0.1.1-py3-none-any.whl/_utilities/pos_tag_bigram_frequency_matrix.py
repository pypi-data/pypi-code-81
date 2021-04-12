import re
from collections import defaultdict

pos_tag_dict = {'Adjective': ('JJ', 'JJR', 'JJS'), 'Noun': ('NN', 'NNS', 'NNP', 'NNPS')}


class POSTagBigramFrequencyMatrix:
    """
    Helps in constructing the POS tag bigram frequency matrix used in computing Conflict, Adjective Absurdity
    """
    def _construct_matrix(self, pos_tagged_corpus_list, first_pos_tag, second_pos_tag):
        for pos_tagged_sent in pos_tagged_corpus_list:
            for i in range(len(pos_tagged_sent) - 1):
                if pos_tagged_sent[i][1] not in pos_tag_dict[first_pos_tag] \
                        or pos_tagged_sent[i + 1][1] not in pos_tag_dict[second_pos_tag]:
                    continue
                first_token = re.sub('[^A-Za-z]*', '', pos_tagged_sent[i][0]).lower()
                second_token = re.sub('[^A-Za-z]*', '', pos_tagged_sent[i + 1][0]).lower()
                self._row_mapping[first_token].add(second_token)
                self._column_mapping[second_token].add(first_token)
                self._table[(first_token, second_token)] += 1
                self._row_keys.add(first_token)
                self._column_keys.add(second_token)

    def __init__(self, pos_tagged_corpus_list, first_pos_tag, second_pos_tag):
        self._row_mapping = defaultdict(set)
        self._column_mapping = defaultdict(set)
        self._table = defaultdict(int)
        self._row_keys = set()
        self._column_keys = set()
        self._construct_matrix(pos_tagged_corpus_list=pos_tagged_corpus_list,
                               first_pos_tag=first_pos_tag,
                               second_pos_tag=second_pos_tag)

    def cell_value(self, word_1: str, word_2: str) -> int:
        return self._table[(word_1, word_2)]

    def get_row(self, word: str) -> set:
        return self._row_mapping[word]

    def get_column(self, word: str) -> set:
        return self._column_mapping[word]

    def get_all_row_keys(self) -> set:
        return self._row_keys

    def get_all_column_keys(self) -> set:
        return self._column_keys
