import re

pos_tag_dict = {'Adjective': ('JJ', 'JJR', 'JJS'), 'Noun': ('NN', 'NNS', 'NNP', 'NNPS')}


class Conflict:
    """Calculates the 'Conflict' metric of a given text"""
    def __init__(self, frequency_matrix):
        self.frequency_matrix = frequency_matrix

    def calculate(self, pos_tags: list) -> float:
        average_conflict = 0.0
        adjective_tags = ('JJ', 'JJR', 'JJS')
        noun_tags = ('NN', 'NNS', 'NNP', 'NNPS')
        frequency_sum = 0
        matches = 0
        for i in range(len(pos_tags) - 1):
            if pos_tags[i][1] in adjective_tags and pos_tags[i + 1][1] in noun_tags:
                adjective = re.sub('[^A-Za-z]*', '', pos_tags[i][0]).lower()
                noun = re.sub('[^A-Za-z]*', '', pos_tags[i + 1][0]).lower()
                frequency_sum += self.frequency_matrix.cell_value(adjective, noun)
                matches += 1
        if matches > 0:
            average_conflict = frequency_sum / matches
        return average_conflict
