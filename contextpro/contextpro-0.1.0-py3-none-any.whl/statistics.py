"""This module contains functions for calculating some text data
related statistics."""

import string
from typing import Any, Dict, Iterable, List, cast

import pandas as pd
from textblob import TextBlob

from contextpro.feature_extraction import ConcurrentCountVectorizer
from contextpro.normalization import batch_lowercase_text, batch_remove_stopwords
from contextpro.processing import (
    Optional,
    Sentence,
    SentenceList,
    is_string_list,
    parallelize_func,
)
from contextpro.tokenization import batch_tokenize_text


def batch_calculate_sentiment_scores(
    documents: SentenceList, num_workers: Optional[int] = None
) -> List[float]:
    """Calculate sentiment scores for sentences in a concurrent manner.

    Parameters
    ----------
    documents : SentenceList
        List of sentences which sentiment scores have to be calculated

    num_workers : Optional[int]
        Number of processors to use, by default None (all processors)

    Returns
    -------
    List[float]
        List of floats within [-1.0, 1.0] range representing sentiment scores
        for the sentences where -1.0 means negative and 1.0 positive

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.statistics import batch_calculate_sentiment_scores
    >>> corpus = [
    ...     "I don't like you.",
    ...     "I love the Spiderman movie",
    ...     "In my opinion this movie was rather boring than exciting",
    ...     "This is the worst movie I've ever seen"
    ... ]
    >>> scores = batch_calculate_sentiment_scores(
    ...     corpus,
    ...     num_workers=2
    ... )
    >>> print(scores)
    [0.0, 0.5, -0.35, -1.0]
    """
    if not is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return cast(
        List[float],
        parallelize_func(
            _calculate_sentiment_score, documents, num_workers=num_workers
        ),
    )


def batch_calculate_subjectivity_scores(
    documents: SentenceList, num_workers: Optional[int] = None
) -> List[float]:
    """Calculate subjectivity scores for sentences in a concurrent manner.

    Parameters
    ----------
    documents : SentenceList
        List of sentences which subjectivity scores have to be calculated

    num_workers : Optional[int]
        Number of processors to use, by default None (all processors)

    Returns
    -------
    List[float]
        List of floats within [0.0, 1.0] range representing subjectivity scores
        for the sentences where 0.0 means very objective and 1.0 very
        subjective

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.statistics import batch_calculate_subjectivity_scores
    >>> corpus = [
    ...     "I don't like you.",
    ...     "I love the Spiderman movie",
    ...     "In my opinion this movie was rather boring than exciting",
    ...     "This is the worst movie I've ever seen"
    ... ]
    >>> scores = batch_calculate_subjectivity_scores(
    ...     corpus,
    ...     num_workers=2
    ... )
    >>> print(scores)
    [0.0, 0.6, 0.9, 1.0]
    """
    if not is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return cast(
        List[float],
        parallelize_func(
            _calculate_subjectivity_score, documents, num_workers=num_workers
        ),
    )


def batch_get_ngram_counts(
    documents: SentenceList,
    ngram_type: str = "unigram",
    lowercase: bool = True,
    remove_stopwords: bool = True,
    num_workers: Optional[int] = None,
) -> Optional[Dict[str, int]]:
    """Count the number of n-grams across the documents corpus in a
    concurrent manner.

    Parameters
    ----------
    documents : SentenceList
        List of strings

    ngram_type : str, optional
        Type of n-grams to count, by default "unigram"

        Allowed values:
          - 'unigram'
          - 'bigram'
          - 'trigram'

    lowercase : bool, optional
        lowercase the documents before deriving unigrams,
        by default True

    remove_stopwords : bool, optional
        remove stopwords before deriving unigrams, by default True

    num_workers : Optional[int], optional
        Number of processors to use, by default None (all processors)

    Returns
    -------
    Optional[Dict[str, int]]
        mapping from unigram to the number of occurrences in corpus

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.statistics import batch_get_ngram_counts
    >>> corpus = [
    ...     "My name is Dr. Jekyll.",
    ...     "His name is Mr. Hyde",
    ...     "This guy's name is Edward Scissorhands",
    ...     "And this is Tom Parker"
    ... ]
    >>> unigrams = batch_get_ngram_counts(
    ...     corpus,
    ...     ngram_type="unigram",
    ...     lowercase=True,
    ...     remove_stopwords=True,
    ...     num_workers=4,
    ... )
    >>> print(unigrams)
    {
        'dr': 1, 'edward': 1, 'guy': 1, 'hyde': 1, 'jekyll': 1,
        'mr': 1, 'name': 3, 'parker': 1, 'scissorhands': 1, 'tom': 1
    }
    >>> bigrams = batch_get_ngram_counts(
    ...     corpus,
    ...     ngram_type="bigram",
    ...     lowercase=True,
    ...     remove_stopwords=True,
    ...     num_workers=4,
    ... )
    >>> print(bigrams)
    {
        'dr jekyll': 1, 'edward scissorhands': 1, 'guy name': 1,
        'mr hyde': 1, 'name dr': 1, 'name edward': 1, 'name mr': 1,
        'tom parker': 1
    }
    >>> trigrams = batch_get_ngram_counts(
    ...     corpus,
    ...     ngram_type="trigram",
    ...     lowercase=True,
    ...     remove_stopwords=True,
    ...     num_workers=2,
    ... )
    >>> print(trigrams)
    {
        'guy name edward': 1, 'name dr jekyll': 1,
        'name edward scissorhands': 1, 'name mr hyde': 1
    }
    """
    if not is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    vectorizer = ConcurrentCountVectorizer(
        lowercase=lowercase,
        remove_stopwords=remove_stopwords,
        ngram_range=(1, 1),
        num_workers=num_workers,
    )
    vectorizer.fit(documents)

    if ngram_type == "unigram":
        return vectorizer.get_unigram_counts()
    elif ngram_type == "bigram":
        return vectorizer.get_bigram_counts()
    else:
        return vectorizer.get_trigram_counts()


def batch_calculate_corpus_statistics(
    documents: SentenceList,
    lowercase: bool = False,
    remove_stopwords: bool = False,
    tokenizer_pattern: str = r"\b[^\d\W]+\b",
    custom_stopwords: List[str] = [],
    num_workers: Optional[int] = None,
) -> pd.DataFrame:
    r"""Calculates the below statistics for each document in the corpus
    in a concurrent manner:

        - Number of characters
        - Number of tokens
        - Number of punctuation characters
        - Number of digits
        - Number of whitespace characters
        - Number of non-ascii characters
        - Sentiment score
        - Subjectivity score

    Parameters
    ----------
    documents : SentenceList
        List of strings

    lowercase : bool, optional
        Convert all characters to lowercase before calculating
        statistics, by default False

    remove_stopwords : bool, optional
        Remove stopwords before calculating statistics. Uses english
        stopwords from the NLTK library if 'custom_stopwords'
        list is not provided, by default False

    tokenizer_pattern : str, optional
        RegEx pattern used by the underlying NLTK Regexp Tokenizer
        to tokenize the documents, by default r"\b[^\d\W]+\b"

    custom_stopwords : List[str], optional
        Custom stopwords to use for token filtering, by default []

    num_workers : Optional[int], optional
        Number of processors to use, by default None (all processors)

    Returns
    -------
    pd.DataFrame
        with statistics for each document in the provided corpus

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.statistics import batch_calculate_corpus_statistics
    >>> corpus = [
    ...     "My name is Dr. Jekyll.",
    ...     "His name is Mr. Hyde",
    ...     "This guy's name is Edward Scissorhands",
    ...     "And this is Tom Parker"
    ... ]
    >>> statistics = batch_calculate_corpus_statistics(
    ...     corpus,
    ...     lowercase=False,
    ...     remove_stopwords=False,
    ...     num_workers=2,
    ... )
    >>> print(statistics)
        characters  tokens  punctuation_characters  digits  whitespace_characters  \
    0          22       5                       2       0                      4
    1          20       5                       1       0                      4
    2          38       7                       1       0                      5
    3          22       5                       0       0                      4

    ascii_characters  sentiment_score  subjectivity_score
    0                22              0.0                 0.0
    1                20              0.0                 0.0
    2                38              0.0                 0.0
    3                22              0.0                 0.0
    """
    if not is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    if lowercase:
        documents = batch_lowercase_text(documents, num_workers=num_workers)

    tokens = batch_tokenize_text(
        documents,
        tokenizer_method="nltk_regexp_tokenizer",
        pattern=tokenizer_pattern,
        gaps=False,
        num_workers=num_workers,
    )

    if remove_stopwords:
        tokens = batch_remove_stopwords(
            tokens, custom_stopwords=custom_stopwords, num_workers=num_workers
        )

    num_chars = _batch_calculate_lengths(documents, num_workers=num_workers)
    num_tokens = _batch_calculate_lengths(tokens, num_workers=num_workers)
    sentiment_scores = batch_calculate_sentiment_scores(
        documents, num_workers=num_workers
    )
    subjectivity_scores = batch_calculate_subjectivity_scores(
        documents, num_workers=num_workers
    )
    num_punct = _batch_calculate_chars(
        documents, character_type="punctuation", num_workers=num_workers
    )
    num_digits = _batch_calculate_chars(
        documents, character_type="digits", num_workers=num_workers
    )
    num_whitespace = _batch_calculate_chars(
        documents, character_type="whitespace", num_workers=num_workers
    )
    num_ascii = _batch_calculate_chars(
        documents, character_type="ascii", num_workers=num_workers
    )

    statistics = pd.DataFrame(
        {
            "characters": num_chars,
            "tokens": num_tokens,
            "punctuation_characters": num_punct,
            "digits": num_digits,
            "whitespace_characters": num_whitespace,
            "ascii_characters": num_ascii,
            "sentiment_score": sentiment_scores,
            "subjectivity_score": subjectivity_scores,
        }
    )

    return statistics


def _calculate_sentiment_score(document: Sentence) -> float:
    """Calculate sentiment score for the sentence using TextBlob object."""
    return float(TextBlob(document).polarity)


def _calculate_subjectivity_score(document: Sentence) -> float:
    """Calculate subjectivity score for the sentence using TextBlob object."""
    return float(TextBlob(document).subjectivity)


def _calculate_chars(document: Sentence, character_type: str = "ascii") -> int:
    """Calculate the number of characters of a chosen type in the document."""
    if character_type == "punctuation":
        chars_to_filter = set(string.punctuation)
    elif character_type == "digits":
        chars_to_filter = set(string.digits)
    elif character_type == "ascii":
        chars_to_filter = set(string.printable)
    elif character_type == "whitespace":
        chars_to_filter = set(string.whitespace)
    count = len(list(filter(lambda char: char in chars_to_filter, document)))
    return count


def _batch_calculate_lengths(
    iterable: Iterable[Any], num_workers: Optional[int] = None
) -> Iterable[int]:
    """Calculate lengths of items in the iterable in a concurrent manner."""
    return parallelize_func(len, iterable, num_workers=num_workers)


def _batch_calculate_chars(
    documents: SentenceList,
    character_type: str = "ascii",
    num_workers: Optional[int] = None,
) -> Iterable[int]:
    """Count the number of characters of a chosen type across the
    document corpus in a concurrent manner.
    """
    return parallelize_func(
        _calculate_chars,
        documents,
        character_type=character_type,
        num_workers=num_workers,
    )


__all__ = [
    "batch_calculate_sentiment_scores",
    "batch_calculate_subjectivity_scores",
    "batch_get_ngram_counts",
    "batch_calculate_corpus_statistics",
]
