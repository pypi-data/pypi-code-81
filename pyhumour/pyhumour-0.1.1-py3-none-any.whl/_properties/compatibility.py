"""Implementation of the Compatibility property."""

from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize


class Compatibility:
    """Calculates the 'Compatibility' value of a given text."""

    @staticmethod
    def calculate(text: str) -> float:
        """Return the 'Compatibility' value of a given text."""
        tokens = word_tokenize(text)
        meanings_positive = 0
        for token in tokens:
            for _ in wordnet.synsets(token):
                meanings_positive += 1

        meanings_average = meanings_positive / len(tokens)
        return meanings_average
