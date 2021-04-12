"""Implementation of the Obviousness property."""

from nltk.tokenize import word_tokenize
from wordfreq import word_frequency


class Obviousness:
    """Calculates the 'Obviousness' value of a given text."""

    @staticmethod
    def calculate(text: str) -> float:
        """Return the 'Obviousness' value of a given text."""
        tokens = word_tokenize(text)
        tokens_average = 0.0
        for token in tokens:
            tokens_average += word_frequency(token, 'en', wordlist='large')
        tokens_average = tokens_average / len(tokens)
        return tokens_average
