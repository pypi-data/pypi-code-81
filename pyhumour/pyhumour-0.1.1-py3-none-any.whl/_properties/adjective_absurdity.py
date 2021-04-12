import re


class AdjectiveAbsurdity:
    """Calculates the 'Adjective Absurdity' metric of a given text"""
    def __init__(self, frequency_matrix):
        self.frequency_matrix = frequency_matrix

    def calculate(self, pos_tags: list) -> float:
        average_adjective_absurdity = 0.0
        adjective_tags = ('JJ', 'JJR', 'JJS')
        noun_tags = ('NN', 'NNS', 'NNP', 'NNPS')
        nouns_list = self.frequency_matrix.get_all_column_keys()
        non_humorous_noun_adj_col_sums = {}
        for noun in nouns_list:
            adjectives_list = self.frequency_matrix.get_column(noun)
            non_humorous_noun_adj_col_sums[noun] = sum(
                [self.frequency_matrix.cell_value(adj, noun) for adj in adjectives_list])
        matches = 0
        freq = 0
        for i in range(len(pos_tags) - 1):
            if pos_tags[i][1] in adjective_tags and pos_tags[i + 1][1] in noun_tags:
                matches += 1
                adjective = re.sub('[^A-Za-z]*', '', pos_tags[i][0]).lower()
                noun = re.sub('[^A-Za-z]*', '', pos_tags[i + 1][0]).lower()
                freq += self.frequency_matrix.cell_value(adjective, noun) / non_humorous_noun_adj_col_sums[noun]
        if matches > 0:
            average_adjective_absurdity = freq / matches
        return average_adjective_absurdity
