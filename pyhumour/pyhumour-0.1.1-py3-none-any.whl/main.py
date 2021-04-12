from nltk.tokenize import word_tokenize
from pyhumour._properties.adjective_absurdity import AdjectiveAbsurdity
from pyhumour._properties.compatibility import Compatibility
from pyhumour._properties.conflict import Conflict
from pyhumour._properties.inappropriateness import Inappropriateness
from pyhumour._properties.language_models import HMMHelper, NgramHelper
from pyhumour._properties.noun_absurdity import NounAbsurdity
from pyhumour._properties.obviousness import Obviousness
from pyhumour._utilities.pos_tag_bigram_frequency_matrix import POSTagBigramFrequencyMatrix
from pyhumour._utilities.preprocess import preprocess_text, preprocess_texts, pos_tag, pos_tag_texts
from pyhumour._utilities.preprocess import preprocess_texts


class PyHumour:
    """
    Core class for PyHumour, with each method representing a
    linguistic feature.
    """

    def __init__(self, humour_corpus: list, non_humour_corpus: list):
        self.humour_corpus = humour_corpus
        self.non_humour_corpus = non_humour_corpus

        # Initialize private variables
        self._obviousness = None
        self._compatibility = None
        self._inappropriateness = None
        self._hmm_trained = None
        self._ngram_trained = None

        self._humorous_adj_noun_matrix = None
        self._non_humorous_adj_noun_matrix = None
        self._pos_tagged_humorous_corpus = None
        self._pos_tagged_non_humorous_corpus = None
        self._humorous_conflict_calculator = None
        self._non_humorous_conflict_calculator = None
        self._adjective_absurdity_calculator = None
        self._humorous_noun_absurdity_calculator = None
        self._non_humorous_noun_absurdity_calculator = None

    def fit(self) -> None:
        self.humour_corpus = preprocess_texts(self.humour_corpus)
        self.non_humour_corpus = preprocess_texts(self.non_humour_corpus)

        self._obviousness = Obviousness()
        self._compatibility = Compatibility()
        self._inappropriateness = Inappropriateness()
        self._hmm_trained = HMMHelper(self.humour_corpus + self.non_humour_corpus)
        self._ngram_trained = NgramHelper(self.humour_corpus)

        self._pos_tagged_humorous_corpus = pos_tag_texts(self.humour_corpus)
        self._pos_tagged_non_humorous_corpus = pos_tag_texts(self.non_humour_corpus)

        self._humorous_adj_noun_matrix = POSTagBigramFrequencyMatrix(
            pos_tagged_corpus_list=self._pos_tagged_humorous_corpus,
            first_pos_tag='Adjective',
            second_pos_tag='Noun')
        self._non_humorous_adj_noun_matrix = POSTagBigramFrequencyMatrix(
            pos_tagged_corpus_list=self._pos_tagged_non_humorous_corpus,
            first_pos_tag='Adjective',
            second_pos_tag='Noun')

        self._humorous_conflict_calculator = Conflict(
            frequency_matrix=self._humorous_adj_noun_matrix)
        self._non_humorous_conflict_calculator = Conflict(
            frequency_matrix=self._non_humorous_adj_noun_matrix)
        self._adjective_absurdity_calculator = AdjectiveAbsurdity(
            frequency_matrix=self._non_humorous_adj_noun_matrix)
        self._humorous_noun_absurdity_calculator = NounAbsurdity(
            frequency_matrix=self._humorous_adj_noun_matrix)
        self._non_humorous_noun_absurdity_calculator = NounAbsurdity(
            frequency_matrix=self._non_humorous_adj_noun_matrix)

    def obviousness(self, text: str) -> float:
        return self._obviousness.calculate(text)

    def compatibility(self, text: str) -> float:
        return self._compatibility.calculate(text)

    def inappropriateness(self, text: str) -> float:
        return self._inappropriateness.calculate(text)

    def humorous_conflict(self, text: str) -> float:
        if self._humorous_conflict_calculator is None:
            raise Exception("Error: Call the fit() method first")

        preprocessed_text = preprocess_text(text)
        pos_tagged_text = pos_tag(word_tokenize(preprocessed_text))

        return self._humorous_conflict_calculator.calculate(pos_tags=pos_tagged_text)

    def non_humorous_conflict(self, text: str) -> float:
        if self._non_humorous_conflict_calculator is None:
            raise Exception("Error: Call the fit() method first")

        preprocessed_text = preprocess_text(text)
        pos_tagged_text = pos_tag(word_tokenize(preprocessed_text))

        return self._non_humorous_conflict_calculator.calculate(pos_tags=pos_tagged_text)

    def adjective_absurdity(self, text: str) -> float:
        if self._adjective_absurdity_calculator is None:
            raise Exception("Error: Call the fit() method first")

        preprocessed_text = preprocess_text(text)
        pos_tagged_text = pos_tag(word_tokenize(preprocessed_text))

        return self._adjective_absurdity_calculator.calculate(pos_tags=pos_tagged_text)

    def humorous_noun_absurdity(self, text: str) -> float:
        if self._humorous_noun_absurdity_calculator is None:
            raise Exception("Error: Call the fit() method first")

        preprocessed_text = preprocess_text(text)
        pos_tagged_text = pos_tag(word_tokenize(preprocessed_text))

        return self._humorous_noun_absurdity_calculator.calculate(pos_tags=pos_tagged_text)

    def non_humorous_noun_absurdity(self, text: str) -> float:
        if self._non_humorous_noun_absurdity_calculator is None:
            raise Exception("Error: Call the fit() method first")

        preprocessed_text = preprocess_text(text)
        pos_tagged_text = pos_tag(word_tokenize(preprocessed_text))

        return self._non_humorous_noun_absurdity_calculator.calculate(pos_tags=pos_tagged_text)

    def hmm_probability(self, text: str) -> float:
        if self._hmm_trained is None:
            # throw error
            raise Exception("Error: Call the fit() method first")
        score = self._hmm_trained.get_hmm_score(text)
        return score

    def ngram_probability(self, text: str) -> float:
        if self._ngram_trained is None:
            raise Exception("Error: Call the fit() method first")
        score = self._ngram_trained.get_ngram_score(text)
        return score
