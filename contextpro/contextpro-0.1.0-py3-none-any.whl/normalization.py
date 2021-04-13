"""This module contains functions for text data normalization."""

import re
import string
from typing import List, Optional, cast

import contractions
import spacy
from nltk.corpus import stopwords
from nltk.stem import (
    LancasterStemmer,
    PorterStemmer,
    RegexpStemmer,
    SnowballStemmer,
    WordNetLemmatizer,
)
from word2number import w2n

from contextpro.processing import (
    NestedTokenList,
    Sentence,
    SentenceList,
    TokenList,
    are_nested_string_lists,
    is_string_list,
    parallelize_func,
)

nlp = spacy.load("en_core_web_sm")


def batch_lowercase_text(
    documents: SentenceList,
    num_workers: Optional[int] = None,
) -> SentenceList:
    """Converts sentences into lowercase in a concurrent manner.

    Parameters
    ----------
    documents : SentenceList
        List of sentences with characters of arbitrary size

    num_workers : Optional[int], optional
        Number of processors to use, by default None (all processors)

    Returns
    -------
    SentenceList
        List of sentences with lowercased characters

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.normalization import batch_lowercase_text
    >>> corpus = [
    ...     "My name is Dr. Jekyll.",
    ...     "His name is Mr. Hyde",
    ...     "This guy's name is Edward Scissorhands",
    ...     "And this is Tom Parker"
    ... ]
    >>> result = batch_lowercase_text(
    ...     corpus,
    ...     num_workers=2
    ... )
    >>> print(result)
    [
        "my name is dr. jekyll.",
        "his name is mr. hyde",
        "this guy's name is edward scissorhands",
        "and this is tom parker"
    ]
    """
    if not is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return cast(
        SentenceList,
        parallelize_func(_lowercase_text, documents, num_workers=num_workers),
    )


def batch_remove_non_ascii_characters(
    documents: SentenceList,
    num_workers: Optional[int] = None,
) -> SentenceList:
    """Removes non-ascii characters from sentences in a concurrent manner.

    Parameters
    ----------
    documents : SentenceList
        List of sentences with non-ascii characters

    num_workers : Optional[int], optional
        Number of processors to use, by default None (all processors)

    Returns
    -------
    SentenceList
        List of sentences with removed non-ascii characters

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.normalization import batch_remove_non_ascii_characters
    >>> corpus = [
    ...     "https://sitebulb.com/Folder/øê.html?大学",
    ...     "J\xf6reskog bi\xdfchen Z\xfcrcher"
    ...     "This is a \xA9 but not a \xAE"
    ...     "fractions \xBC, \xBD, \xBE"
    ... ]
    >>> result = batch_remove_non_ascii_characters(
    ...     corpus,
    ...     num_workers=2
    ... )
    >>> print(result)
    [
        'https://sitebulb.com/Folder/.html?',
        'Jreskog bichen Zrcher',
        'This is a  but not a ',
        'fractions , , '
    ]
    """
    if not is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return cast(
        SentenceList,
        parallelize_func(
            _remove_non_ascii_characters, documents, num_workers=num_workers
        ),
    )


def batch_replace_contractions(
    documents: SentenceList, num_workers: Optional[int] = None, **kwargs
) -> SentenceList:
    """Expands the contractions in sentences in a concurrent manner.

    Parameters
    ----------
    documents : SentenceList
        List of sentences with contracted words

    num_workers : Optional[int]
        Number of processors to use, by default None (all processors)

    Other Parameters
    ----------------
    **kwargs : Additional properties of the below method:
      - contractions.fix()

    Returns
    -------
    SentenceList
        List of sentences without contractions

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.normalization import batch_replace_contractions
    >>> corpus = [
    ...     "I don't want to be rude, but you shouldn't do this",
    ...     "Do you think he'll pass his driving test?",
    ...     "I'll see you next week",
    ...     "I'm going for a walk"
    ... ]
    >>> result = batch_replace_contractions(
    ...     corpus,
    ...     num_workers=2
    ... )
    >>> print(result)
    [
        'I do not want to be rude, but you should not do this',
        'Do you think he will pass his driving test?',
        'I will see you next week',
        'I am going for a walk',
    ]
    """
    if not is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return cast(
        SentenceList,
        parallelize_func(
            _replace_contractions, documents, num_workers=num_workers, **kwargs
        ),
    )


def batch_remove_stopwords(
    tokens: NestedTokenList,
    custom_stopwords: List[str] = [],
    num_workers: Optional[int] = None,
) -> NestedTokenList:
    """Removes stopwords from lists of tokens in a concurrent manner.

    Parameters
    ----------
    tokens : NestedTokenList
        List of lists of tokens with stopwords

    custom_stopwords: List[str], optional
        List of stopwords to remove from sentences, by default []

    num_workers : Optional[int], optional
        Number of processors to use, by default None (all processors)

    Returns
    -------
    NestedTokenList
        List of lists of tokens without stopwords

    Raises
    ------
    ValueError
        if 'tokens' provided are not a list of nested string lists

    Examples
    --------
    >>> from contextpro.normalization import batch_remove_stopwords
    >>> corpus = [
    ...     ['My', 'name', 'is', 'Dr', 'Jekyll'],
    ...     ['His', 'name', 'is', 'Mr', 'Hyde'],
    ...     ['This', 'guy', 's', 'name', 'is', 'Edward', 'Scissorhands'],
    ...     ['And', 'this', 'is', 'Tom', 'Parker']
    ... ]
    >>> result = batch_remove_stopwords(
    ...     corpus,
    ...     num_workers=2
    ... )
    >>> print(result)
    [
        ['My', 'name', 'Dr', 'Jekyll'],
        ['His', 'name', 'Mr', 'Hyde'],
        ['This', 'guy', 'name', 'Edward', 'Scissorhands'],
        ['And', 'Tom', 'Parker']
    ]
    """
    if not are_nested_string_lists(tokens):
        raise ValueError("'tokens' should be a list of nested string lists")

    return cast(
        NestedTokenList,
        parallelize_func(
            _remove_stopwords,
            tokens,
            custom_stopwords=custom_stopwords,
            num_workers=num_workers,
        ),
    )


def batch_stem(
    tokens: NestedTokenList,
    stemmer_type: Optional[str] = "nltk_porter_stemmer",
    num_workers: Optional[int] = None,
    **kwargs,
) -> NestedTokenList:
    """Stems tokens in lists of tokens to their root (base) form in a
    concurrent manner.

    Parameters
    ----------
    tokens : NestedTokenList
        List of lists of tokens containing words with various
        inflectional forms

    stemmer_type : Optional[str], optional
        Stemmer instance which will be used to stem the tokens,
        by default "nltk_porter_stemmer"

        Allowed values:
          - nltk_porter_stemmer
          - nltk_lancaster_stemmer
          - nltk_regexp_stemmer
          - nltk_snowball_stemmer

    num_workers : Optional[int], optional
        Number of processors to use, by default None (all processors)

    Other Parameters
    ----------------
    **kwargs : Additional properties of the below stemmers:

      - nltk.PorterStemmer
      - nltk.LancasterStemmer
      - nltk.RegexpStemmer
      - nltk.SnowballStemmer

    Returns
    -------
    NestedTokenList
        List of lists of stemmed tokens

    Raises
    ------
    ValueError
        if 'tokens' provided are not a list of nested string lists

    Examples
    --------
    >>> from contextpro.normalization import batch_stem
    >>> corpus =  [
    ...     ["I", "like", "driving", "a", "car"],
    ...     ["I", "am", "going", "for", "a", "walk"],
    ...     ["Do", "you", "think", "this", "is", "doable"],
    ...     ["I", "have", "three", "bikes", "in", "two", "garages"]
    ... ]
    >>> result = batch_stem(
    ...    corpus,
    ...    stemmer_type="nltk_porter_stemmer",
    ...    num_workers=2
    ... )
    >>> print(result)
    [
        ['I', 'like', 'drive', 'a', 'car'],
        ['I', 'am', 'go', 'for', 'a', 'walk'],
        ['Do', 'you', 'think', 'thi', 'is', 'doabl'],
        ['I', 'have', 'three', 'bike', 'in', 'two', 'garag']
    ]
    """
    if not are_nested_string_lists(tokens):
        raise ValueError("'tokens' should be a list of nested string lists")

    return cast(
        NestedTokenList,
        parallelize_func(
            _stem,
            tokens,
            stemmer_type=stemmer_type,
            num_workers=num_workers,
            **kwargs,
        ),
    )


def batch_lemmatize(
    tokens: NestedTokenList,
    num_workers: Optional[int] = None,
    **kwargs,
) -> NestedTokenList:
    """Lemmatizes tokens in lists of tokens in a concurrent manner using
    NLTK WordNetLemmatizer.

    Parameters
    ----------
    tokens : NestedTokenList
        List of lists of tokens containing words with various
        inflectional forms

    num_workers : Optional[int], optional
        Number of processors to use, by default None (all processors)

    Other Parameters
    ----------------
    **kwargs : Additional properties of the below lemmatizer:

      - nltk.WordNetLemmatizer

    Returns
    -------
    NestedTokenList
        List of lists of lemmatized tokens

    Raises
    ------
    ValueError
        if 'tokens' provided are not a list of nested string lists

    Examples
    --------
    >>> from contextpro.normalization import batch_lemmatize
    >>> corpus =  [
    ...     ["I", "like", "driving", "a", "car"],
    ...     ["I", "am", "going", "for", "a", "walk"],
    ...     ["What", "are", "you", "doing"],
    ...     ["Where", "are", "you", "coming", "from"]
    ... ]
    >>> result = batch_lemmatize(
    ...    corpus,
    ...    num_workers=2,
    ...    pos="v"
    ... )
    >>> print(result)
    [
        ['I', 'like', 'drive', 'a', 'car'],
        ['I', 'be', 'go', 'for', 'a', 'walk'],
        ['What', 'be', 'you', 'do'],
        ['Where', 'be', 'you', 'come', 'from']
    ]
    """
    if not are_nested_string_lists(tokens):
        raise ValueError("'tokens' should be a list of nested string lists")

    return cast(
        NestedTokenList,
        parallelize_func(_lemmatize, tokens, num_workers=num_workers, **kwargs),
    )


def batch_remove_punctuation(
    documents: SentenceList, num_workers: Optional[int] = None
) -> SentenceList:
    """Removes punctuation characters from all sentences in a concurrent manner.

    Parameters
    ----------
    documents : SentenceList
        List of sentences which contain punctuation characters

    num_workers : Optional[int]
        Number of processors to use, by default None (all processors)

    Returns
    -------
    SentenceList
        List of sentences without punctuation characters

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.normalization import batch_remove_punctuation
    >>> corpus = [
    ...     "My name is Dr. Jekyll.",
    ...     "His name is Mr. Hyde!",
    ...     "Is his name Edward Scissorhands?",
    ...     "This is Tom-Parker!"
    ... ]
    >>> result = batch_remove_punctuation(
    ...     corpus,
    ...     num_workers=2
    ... )
    >>> print(result)
    [
        'My name is Dr Jekyll',
        'His name is Mr Hyde',
        'Is his name Edward Scissorhands',
        'This is TomParker'
    ]
    """
    if not is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return cast(
        SentenceList,
        parallelize_func(_remove_punctuation, documents, num_workers=num_workers),
    )


def batch_remove_numbers(
    documents: SentenceList, num_workers: Optional[int] = None
) -> SentenceList:
    """Removes numbers from all sentences in a concurrent manner.

    Parameters
    ----------
    documents : SentenceList
        List of sentences which contain numbers

    num_workers : Optional[int]
        Number of processors to use, by default None (all processors)

    Returns
    -------
    SentenceList
        List of sentences without numbers

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.normalization import batch_remove_numbers
    >>> corpus = [
    ...     "He is 12 years old.",
    ...     "His father has 3 cars",
    ...     "I have 3 computers",
    ...     "He earns 1000$ daily"
    ... ]
    >>> result = batch_remove_numbers(
    ...     corpus,
    ...     num_workers=2
    ... )
    >>> print(result)
    [
        'He is  years old.',
        'His father has  cars',
        'I have  computers',
        'He earns $ daily'
    ]
    """
    if not is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return cast(
        SentenceList,
        parallelize_func(_remove_numbers, documents, num_workers=num_workers),
    )


def batch_remove_whitespace(
    documents: SentenceList, num_workers: Optional[int] = None
) -> SentenceList:
    r"""Removes whitespace characters from all sentences in a concurrent manner.

    Parameters
    ----------
    documents : SentenceList
        List of sentences which contain whitespace characters

    num_workers : Optional[int]
        Number of processors to use, by default None (all processors)

    Returns
    -------
    SentenceList
        List of sentences without whitespace characters

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.normalization import batch_remove_whitespace
    >>> corpus = [
    ...     "He Has Not Been    in Touch for over a Month.",
    ...     "I Will See \r\nYou next Week",,
    ...     "I Am Hungry - Can We\t Eat Now, Please?",,
    ...     "It Is \r\nFreezing Outside!"
    ... ]
    >>> result = batch_remove_whitespace(
    ...     corpus,
    ...     num_workers=2
    ... )
    >>> print(result)
    [
        'He Has Not Been in Touch for over a Month.',
        'I Will See You next Week',
        'I Am Hungry - Can We Eat Now, Please?',
        'It Is Freezing Outside!',
    ]
    """
    if not is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return cast(
        SentenceList,
        parallelize_func(_remove_whitespace, documents, num_workers=num_workers),
    )


def batch_convert_numerals_to_numbers(
    documents: SentenceList, num_workers: Optional[int] = None
) -> SentenceList:
    """Replaces numerals with numbers in all sentences in a concurrent manner.

    Parameters
    ----------
    documents : SentenceList
        List of sentences which contain numerals

    num_workers : Optional[int]
        Number of processors to use, by default None (all processors)

    Returns
    -------
    SentenceList
        List of sentences with numerals converted to numbers

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.normalization import batch_convert_numerals_to_numbers
    >>> corpus = [
    ...     "A bunch of five",
    ...     "A picture is worth a thousand words",
    ...     "A stitch in time saves nine",
    ...     "Back to square one",
    ...     "Behind the eight ball",
    ...     "Between two stools",
    ... ]
    >>> result = batch_convert_numerals_to_numbers(
    ...     corpus,
    ...     num_workers=2
    ... )
    >>> print(result)
    [
        'A bunch of 5',
        'A picture is worth a 1000 words',
        'A stitch in time saves 9',
        'Back to square 1',
        'Behind the 8 ball',
        'Between 2 stools',
    ]
    """
    if not is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return cast(
        SentenceList,
        parallelize_func(
            _convert_numerals_to_digits, documents, num_workers=num_workers
        ),
    )


def _remove_stopwords(tokens: TokenList, custom_stopwords: List[str] = []) -> TokenList:
    """Removes stopwords from the provided list of tokens."""

    if custom_stopwords:
        stop_words = set(custom_stopwords)
    else:
        stop_words = set(stopwords.words("english"))
    return cast(TokenList, [word for word in tokens if word not in stop_words])


def _remove_non_ascii_characters(document: Sentence) -> Sentence:
    """Removes non-ascii characters from the provided sentence."""
    printable_chars = set(string.printable)
    return cast(
        Sentence, "".join(filter(lambda char: char in printable_chars, document))
    )


def _remove_punctuation(document: Sentence) -> Sentence:
    """Removes punctuation characters from the sentence."""
    punctuation_chars = set(string.punctuation)
    return cast(
        Sentence, "".join(filter(lambda char: char not in punctuation_chars, document))
    )


def _remove_numbers(document: Sentence) -> Sentence:
    """Removes numbers from the sentence."""
    digit_chars = set(string.digits)
    return cast(
        Sentence, "".join(filter(lambda char: char not in digit_chars, document))
    )


def _remove_whitespace(document: Sentence) -> Sentence:
    """Removes whitespace characters from the sentence."""
    return cast(Sentence, " ".join(re.split(r"\s+", document, flags=re.UNICODE)))


def _convert_numerals_to_digits(document: Sentence) -> Sentence:
    """Replaces numerals with numbers in a sentence."""
    spacy_doc = nlp(document)
    tokens = [
        w2n.word_to_num(token.text) if token.pos_ == "NUM" else token.text
        for token in spacy_doc
    ]

    return cast(Sentence, " ".join([str(token) for token in tokens]))


def _replace_contractions(document: Sentence, **kwargs) -> Sentence:
    """Expands the contractions in a sentence."""
    return cast(Sentence, contractions.fix(document, **kwargs))


def _lowercase_text(document: Sentence) -> Sentence:
    """Converts the sentence to lowercase."""
    return cast(Sentence, document.lower())


def _stem(
    tokens: TokenList, stemmer_type: Optional[str] = "nltk_porter_stemmer", **kwargs
) -> TokenList:
    """Reduces tokens to their root (base) form."""

    if stemmer_type == "nltk_porter_stemmer":  # pragma: no cover
        stemmer = PorterStemmer(**kwargs)
    elif stemmer_type == "nltk_lancaster_stemmer":  # pragma: no cover
        stemmer = LancasterStemmer(**kwargs)
    elif stemmer_type == "nltk_regexp_stemmer":  # pragma: no cover
        stemmer = RegexpStemmer(**kwargs)
    else:  # pragma: no cover
        stemmer = SnowballStemmer(**kwargs)

    return cast(TokenList, [stemmer.stem(word) for word in tokens])  # pragma: no cover


def _lemmatize(
    tokens: TokenList,
    **kwargs,
) -> TokenList:
    """Lemmatize tokens using NLTK's WordNetLemmatizer"""
    lemmatizer = WordNetLemmatizer()  # pragma: no cover
    return cast(
        TokenList, [lemmatizer.lemmatize(word, **kwargs) for word in tokens]
    )  # pragma: no cover


_all_ = [
    "batch_lowercase_text",
    "batch_remove_non_ascii_characters",
    "batch_replace_contractions",
    "batch_remove_stopwords",
    "batch_stem",
    "batch_lemmatize",
    "batch_remove_punctuation",
    "batch_remove_numbers",
    "batch_remove_whitespace",
    "batch_convert_numerals_to_numbers",
]
