"""This module contains classes and functions for extracting features
from text data."""

from itertools import zip_longest
from typing import Dict, List, Optional, Tuple, cast

import numpy as np
import scipy.sparse as sp
from nltk.probability import FreqDist

from contextpro.exceptions import NotFitted
from contextpro.normalization import batch_lowercase_text, batch_remove_stopwords
from contextpro.processing import (
    NestedTokenList,
    SentenceList,
    TokenList,
    are_nested_string_lists,
    is_string_list,
    parallelize_func,
)
from contextpro.tokenization import batch_tokenize_text


class ConcurrentCountVectorizer:
    r"""Convert a collection of text documents to a matrix of token counts.

    This implementation produces a sparse representation of the counts using
    scipy.sparse.csr_matrix.

    Parameters
    ----------
    lowercase : bool, optional
        Convert all characters to lowercase before tokenizing

    remove_stopwords : bool, optional
        Remove stopwords. Uses english stopwords from the NLTK
        library, by default False

    ngram_range : Tuple[int, int], optional
        The lower and upper boundary of the range of n-grams
        to be extracted and included in the vocabulary.

            - (1, 1) means only unigrams
            - (1, 2) means unigrams and bigrams
            - (2, 2) means only bigrams
            - (2, 3) means bigrams and trigrams
            - (1, 3) means unigrams, bigrams and trigrams

    tokenizer_pattern : str, optional
        RegEx pattern used by the underlying NLTK Regexp Tokenizer
        to tokenize the documents, by default r"\b[^\d\W]+\b"

    num_workers : Optional[int], optional
        Number of processors to use, by default None (all processors)

    Examples
    --------
    >>> from contextpro.feature_extraction import ConcurrentCountVectorizer
    >>> corpus = [
    ...     "My name is Dr. Jekyll.",
    ...     "His name is Mr. Hyde",
    ...     "This guy's name is Edward Scissorhands",
    ...     "And this is Tom Parker"
    ... ]
    >>> cvv = ConcurrentCountVectorizer(
    ...     lowercase=True,
    ...     remove_stopwords=True,
    ...     ngram_range=(1, 1),
    ...     num_workers=2
    ... )
    >>> transformed = cvv.fit_transform(corpus)
    >>> print(cvv.get_feature_names())
    [
        'dr', 'edward', 'guy', 'hyde', 'jekyll', 'mr',
        'name', 'parker', 'scissorhands', 'tom'
    ]
    >>> print(transformed.toarray())
    [
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 1]
    ]
    """

    def __init__(
        self,
        lowercase: bool = True,
        remove_stopwords: bool = True,
        ngram_range: Tuple[int, int] = (1, 1),
        tokenizer_pattern: str = r"\b[^\d\W]+\b",
        num_workers: Optional[int] = None,
    ):
        self.lowercase = lowercase
        self.remove_stopwords = remove_stopwords
        self.tokenizer_pattern = tokenizer_pattern
        self.num_workers = num_workers
        self.ngram_range = ngram_range
        self.documents = None
        self.tokens = None
        self.vocabulary = None

    @property
    def lowercase(self) -> bool:
        """Lowercase the documents before learning the vocabulary.

        Returns
        -------
        bool
            True if documents should be lowercased before learning the
            vocabulary, False otherwise
        """
        return self._lowercase

    @lowercase.setter
    def lowercase(self, value: bool):
        if isinstance(value, bool):
            self._lowercase = value
        else:
            raise ValueError(
                (
                    "Invalid value provided for the 'lowercase' "
                    f"parameter. Expected bool, got {type(value)}"
                )
            )

    @property
    def remove_stopwords(self) -> bool:
        """Remove stopwords before learning the vocabulary.

        Returns
        -------
        bool
            True if stopwords should be removed from the documents
            before learning the vocabulary, False otherwise
        """
        return self._remove_stopwords

    @remove_stopwords.setter
    def remove_stopwords(self, value: bool):
        if isinstance(value, bool):
            self._remove_stopwords = value
        else:
            raise ValueError(
                (
                    "Invalid value provided for the 'remove_stopwords' "
                    f"parameter. Expected bool, got {type(value)}"
                )
            )

    @property
    def tokenizer_pattern(self) -> str:
        """Regex pattern (raw string) for the underlying tokenizer -
        NLTK RegexpTokenizer

        Returns
        -------
        str
            Regexp pattern used for tokenization
        """
        return self._tokenizer_pattern

    @tokenizer_pattern.setter
    def tokenizer_pattern(self, value: str):
        if isinstance(value, str):
            self._tokenizer_pattern = value
        else:
            raise ValueError(
                (
                    "Invalid value provided for the 'tokenizer_pattern' "
                    f"parameter. Expected str, got {type(value)}"
                )
            )

    @property
    def num_workers(self) -> Optional[int]:
        """Number of concurrent processes to use for preprocessing the
        documents and creating a document-term matrix. Used to decrease
        the required processing time.

        Returns
        -------
        Optional[int]
            Number of concurrent processes, by default None,
            which means use all available logical processor cores.
        """
        return self._num_workers

    @num_workers.setter
    def num_workers(self, value: int):
        self._num_workers: Optional[int] = None
        if isinstance(value, type(None)):
            pass
        elif isinstance(value, int):
            self._num_workers = value
        else:
            raise ValueError(
                (
                    "Invalid value provided for the 'num_workers' "
                    f"parameter. Expected int, got {type(value)}"
                )
            )

    @property
    def ngram_range(self) -> Tuple[int, int]:
        """The lower and upper boundary of the range of n-grams
        to be extracted and included in the vocabulary.

            - (1, 1) means only unigrams
            - (1, 2) means unigrams and bigrams
            - (2, 2) means only bigrams
            - (2, 3) means bigrams and trigrams
            - (1, 3) means unigrams, bigrams and trigrams

        Returns
        -------
        Tuple[int, int]
            representing lower and upper boundary for the range
            of n-grams to include in the vocabulary and transformed
            documents
        """
        return self._ngram_range

    @ngram_range.setter
    def ngram_range(self, value: Tuple[int, int]):
        if not isinstance(value, tuple):
            raise TypeError(f"'ngram_range' should be a tuple, got {type(value)}")
        if not all(isinstance(boundary, int) for boundary in value) and len(value) == 2:
            raise ValueError("'ngram_range' should contain 2 integers.")

        lowerbound, upperbound = value

        if not 1 <= lowerbound <= 3 or not 1 <= upperbound <= 3:
            raise ValueError("'ngram_range' bounds must be between 1 and 3")

        self._ngram_range = value

    @property
    def documents(self) -> Optional[SentenceList]:
        """Documents used to train the vectorizer and build
        its vocabulary.

        Returns
        -------
        Optional[SentenceList]
            List of documents to learn the vocabulary from

        Raises
        ------
        NotFitted
            if vectorizer was not fitted using either 'fit()' or
            'fit_transform()' method
        """
        if self._documents:
            return self._documents
        else:
            raise NotFitted("Vectorizer not fitted. Call 'fit()'method first")

    @documents.setter
    def documents(self, value: SentenceList):
        if is_string_list(value):
            self._documents = SentenceList(value)

    @property
    def tokens(self) -> Optional[NestedTokenList]:
        """Nested token lists generated from the provided corpus of
        documents.

        Returns
        -------
        Optional[NestedTokenList]
            List of lists where each nested list represents a tokenized
            document.

        Raises
        ------
        NotFitted
            if vectorizer was not fitted using either 'fit()' or
            'fit_transform()' method
        """
        if self._tokens:
            return self._tokens
        else:
            raise NotFitted("Vectorizer not fitted. Call 'fit()'method first")

    @tokens.setter
    def tokens(self, value: NestedTokenList):
        if are_nested_string_lists(value):
            self._tokens = NestedTokenList(value)

    @property
    def vocabulary(self) -> Optional[Dict[str, int]]:
        """Vocabulary learnt from the provided corpus of documents.

        Returns
        -------
        Optional[Dict[str, int]]
            Mapping from token(ngram) to its number in the vocabulary
            dictionary

        Raises
        ------
        NotFitted
            if vectorizer was not fitted using either 'fit()' or
            'fit_transform()' method
        """
        if self._vocabulary:
            return self._vocabulary
        else:
            raise NotFitted("Vectorizer not fitted. Call 'fit()'method first")

    @vocabulary.setter
    def vocabulary(self, value: Optional[Dict[str, int]]):
        self._vocabulary: Optional[Dict[str, int]] = None
        if isinstance(value, dict):
            if all(isinstance(key, str) for key in value.keys()) and all(
                isinstance(val, int) for val in value.values()
            ):
                self._vocabulary = value

    def fit(self, documents: SentenceList):
        """Preprocess the documents and learn vocabulary.

        Parameters
        ----------
        documents : SentenceList
            List of documents to learn the vocabulary from

        Raises
        ------
        ValueError
            if not all elements of the 'documents' list are strings
        """
        if not is_string_list(documents):
            raise ValueError("'documents' should be a list of strings")

        self.documents = documents
        self.tokens = self._preprocess_documents(documents)
        self._build_vocabulary()

    def transform(self, documents: SentenceList) -> sp.csr_matrix:
        """Transform documents into a document-term matrix.

        Parameters
        ----------
        documents : SentenceList
            List of documents to transform

        Returns
        -------
        sp.csr_matrix
            sparse document-term matrix of shape (n_samples, n_features)

        Raises
        ------
        ValueError
            if not all elements of the 'documents' list are strings
        """
        if not is_string_list(documents):
            raise ValueError("'documents' should be a list of strings")

        docs = self._preprocess_documents(documents)
        docs = self._docs_to_ngrams(docs)
        docs = self._docs_to_matrix(docs)
        docs_matrix = sp.csr_matrix(np.hstack(docs).T, dtype=np.uint32)
        return docs_matrix

    def fit_transform(self, documents: SentenceList) -> sp.csr_matrix:
        """Learn the vocabulary dictionary from the provided document
        corpus and transform it into a document-term matrix.

        Parameters
        ----------
        documents : SentenceList
            List of documents to learn the vocabulary from and transform

        Returns
        -------
        sp.csr_matrix
            sparse document-term matrix of shape (n_samples, n_features)

        Raises
        ------
        ValueError
            if not all elements of the 'documents' list are strings
        """
        if not is_string_list(documents):
            raise ValueError("'documents' should be a list of strings")

        self.fit(documents)
        return self.transform(documents)

    def get_feature_names(self) -> List[str]:
        """Return a list of feature names as exist in vocabulary.

        Returns
        -------
        List[str]
            list of feature names from the learnt vocabulary

        Raises
        ------
        NotFitted
            if vectorizer was not fitted using either 'fit()' or
            'fit_transform()' method
        """
        if self.vocabulary:
            return list(self.vocabulary.keys())
        else:
            raise NotFitted("Call 'fit()' or 'fit_transform()' method first")

    def get_unigram_counts(self) -> Optional[Dict[str, int]]:
        """Calculate unigram counts in corpus.

        Returns
        -------
        Optional[Dict[str, int]]
            mapping from unigram to the number of occurrences in corpus

        Raises
        ------
        NotFitted
            if vectorizer was not fitted using either 'fit()' or
            'fit_transform()' method with adequate value for
            'ngram_range' parameter
        """
        if self.tokens:
            return self._count_grams(self.get_unigrams(self.tokens))
        else:
            raise NotFitted(
                (
                    "Call 'fit()' or 'fit_transform()' method with "
                    "adequate 'ngram_range' first"
                )
            )

    def get_bigram_counts(self) -> Optional[Dict[str, int]]:
        """Calculate bigram counts in corpus.

        Returns
        -------
        Optional[Dict[str, int]]
            mapping from bigram to the number of occurrences in corpus

        Raises
        ------
        NotFitted
            if vectorizer was not fitted using either 'fit()' or
            'fit_transform()' method with adequate value for
            'ngram_range' parameter
        """
        if self.tokens:
            return self._count_grams(self.get_bigrams(self.tokens))
        else:
            raise NotFitted(
                (
                    "Call 'fit()' or 'fit_transform()' method with "
                    "adequate 'ngram_range' first"
                )
            )

    def get_trigram_counts(self) -> Optional[Dict[str, int]]:
        """Calculate trigram counts in corpus.

        Returns
        -------
        Optional[Dict[str, int]]
            mapping from trigram to the number of occurrences in corpus

        Raises
        ------
        NotFitted
            if vectorizer was not fitted using either 'fit()' or
            'fit_transform()' method with adequate value for
            'ngram_range' parameter
        """
        if self.tokens:
            return self._count_grams(self.get_trigrams(self.tokens))
        else:
            raise NotFitted(
                (
                    "Call 'fit()' or 'fit_transform()' method with "
                    "adequate 'ngram_range' first"
                )
            )

    @staticmethod
    def get_ngrams(tokens: TokenList, n: int = 1) -> TokenList:
        """Prepare n-grams from the provided list of tokens.

        Parameters
        ----------
        tokens : TokenList
            List of tokens representing single document
        n : int, optional
            Type of n-grams to produce, by default 1 (unigram)

        Returns
        -------
        TokenList
            List of n-grams

        Raises
        ------
        ValueError
            if 'tokens' provided is not a list of strings
        """
        if not is_string_list(tokens):
            raise ValueError("'tokens' should be a list of nested string lists")

        ngrams = []
        for num in range(0, len(tokens)):
            ngram = " ".join(tokens[num : num + n])
            ngrams.append(ngram)
        return cast(
            TokenList, [ngram for ngram in ngrams if len(ngram.split(" ")) == n]
        )

    def get_unigrams(self, tokens: NestedTokenList) -> NestedTokenList:
        """Prepare unigrams from the nested token lists.

        Parameters
        ----------
        tokens : NestedTokenList
            List of token lists, each representing single document

        Returns
        -------
        NestedTokenList
            List of lists of unigrams, each representing single document

        Raises
        ------
        ValueError
            if 'tokens' provided are not a list of nested string lists
        """
        if not are_nested_string_lists(tokens):
            raise ValueError("'tokens' should be a list of nested string lists")

        unigrams = parallelize_func(
            self.get_ngrams, tokens, n=1, num_workers=self.num_workers
        )

        return cast(NestedTokenList, unigrams)

    def get_bigrams(self, tokens: NestedTokenList) -> NestedTokenList:
        """Prepare bigrams from the nested token lists.

        Parameters
        ----------
        tokens : NestedTokenList
            List of token lists, each representing single document

        Returns
        -------
        NestedTokenList
            List of lists of bigrams, each representing single document

        Raises
        ------
        ValueError
            if 'tokens' provided are not a list of nested string lists
        """
        if not are_nested_string_lists(tokens):
            raise ValueError("'tokens' should be a list of nested string lists")

        bigrams = parallelize_func(
            self.get_ngrams, tokens, n=2, num_workers=self.num_workers
        )
        return cast(NestedTokenList, bigrams)

    def get_trigrams(self, tokens: NestedTokenList) -> NestedTokenList:
        """Prepare trigrams from the nested token lists.

        Parameters
        ----------
        tokens : NestedTokenList
            List of token lists, each representing single document

        Returns
        -------
        NestedTokenList
            List of lists of trigrams, each representing single document

        Raises
        ------
        ValueError
            if 'tokens' provided are not a list of nested string lists
        """
        if not are_nested_string_lists(tokens):
            raise ValueError("'tokens' should be a list of nested string lists")

        trigrams = parallelize_func(
            self.get_ngrams, tokens, n=3, num_workers=self.num_workers
        )
        return cast(NestedTokenList, trigrams)

    def _preprocess_documents(self, documents: SentenceList) -> NestedTokenList:
        """Apply preprocessing methods to the provided document corpus"""
        if self.lowercase:
            documents = batch_lowercase_text(documents, num_workers=self.num_workers)
        tokens = batch_tokenize_text(
            documents,
            tokenizer_method="nltk_regexp_tokenizer",
            num_workers=self.num_workers,
            pattern=self.tokenizer_pattern,
            gaps=False,
        )
        if self.remove_stopwords:
            tokens = batch_remove_stopwords(tokens, num_workers=self.num_workers)

        return tokens

    def _count_grams(self, ngrams: NestedTokenList) -> Dict[str, int]:
        """Count number of unique n-grams"""
        flat_grams = [ngram for doc in ngrams for ngram in doc]
        dist = FreqDist(flat_grams)
        return {ngram: count for ngram, count in zip(dist.keys(), dist.values())}

    def _build_vocabulary(self):
        """Build n-gram vocabulary"""
        ngrams = self._docs_to_ngrams(self.tokens)
        flat_ngrams = sorted(set([ngram for doc in ngrams for ngram in doc]))
        self.vocabulary = {ngram: idx for idx, ngram in enumerate(flat_ngrams)}

    def _docs_to_ngrams(self, tokens: NestedTokenList) -> NestedTokenList:
        """Represent tokenized documents as n-gram lists."""
        return cast(
            NestedTokenList,
            parallelize_func(self._doc_to_ngrams, tokens, num_workers=self.num_workers),
        )

    def _docs_to_matrix(self, tokens: NestedTokenList):
        """Represent tokenized documents as document-term matrix."""
        return parallelize_func(
            self._doc_to_matrix, tokens, num_workers=self.num_workers
        )

    def _doc_to_ngrams(self, tokens: TokenList) -> TokenList:
        """Represent tokenized document as n-gram list."""
        ngram_range = range(self.ngram_range[0], self.ngram_range[1] + 1)
        ngrams = [self.get_ngrams(tokens, n) for n in ngram_range]
        doc = [
            ngram
            for joined_ngrams in list(zip_longest(*ngrams, fillvalue=""))
            for ngram in joined_ngrams
            if ngram != ""
        ]
        return cast(TokenList, doc)

    def _doc_to_matrix(self, tokens: TokenList):
        """Represent tokenized document as a vector of n-gram counts."""
        if not self.vocabulary:
            raise NotFitted("Vectorizer not fitted. Call 'fit()'method first")

        feature_counter = {}
        for token in tokens:
            try:
                feature_idx = self.vocabulary[token]
                if feature_idx not in feature_counter:
                    feature_counter[feature_idx] = 1
                else:
                    feature_counter[feature_idx] += 1
            except KeyError:
                continue

        matrix = np.zeros((len(self.vocabulary), 1), dtype=np.uint16)
        features = np.array(list(feature_counter.keys()))
        counts = np.array(list(feature_counter.values()))
        for feat, count in zip(features, counts):
            matrix[feat] = count
        return matrix


__all__ = ["ConcurrentCountVectorizer"]
