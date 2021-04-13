"""This module contains functions used for text data tokenization."""

from typing import Optional, cast

import nltk

from contextpro.processing import (
    NestedTokenList,
    Sentence,
    SentenceList,
    TokenList,
    is_string_list,
    parallelize_func,
)


def batch_tokenize_text(
    documents: SentenceList,
    tokenizer_method: Optional[str] = "nltk_word_tokenizer",
    num_workers: Optional[int] = None,
    **kwargs,
) -> NestedTokenList:
    r"""Tokenizes sentences in a concurrent manner.

    Parameters
    ----------
    documents : SentenceList
        List of sentences to tokenize

    tokenizer_method : Optional[str]
        Tokenization method which will be used to tokenize the sentences
        by default "nltk_word_tokenizer".

        Allowed values:
          - nltk_word_tokenizer
          - nltk_regexp_tokenizer

    num_workers : Optional[int], optional
        Number of processors to use, by default None (all processors)

    Other Parameters
    ----------------
    **kwargs : Additional properties of the below methods:

      - nltk.word_tokenize()
      - nltk.regexp_tokenize()

    Returns
    -------
    NestedTokenList
        List of lists of tokens

    Raises
    ------
    ValueError
        if 'documents' provided are not a list of strings

    Examples
    --------
    >>> from contextpro.tokenization import batch_tokenize_text
    >>> corpus = [
    ...     "My name is Dr. Jekyll.",
    ...     "His name is Mr. Hyde",
    ...     "This guy's name is Edward Scissorhands",
    ...     "And this is Tom Parker"
    ... ]
    >>> tokens = batch_tokenize_text(
    ...     corpus,
    ...     tokenizer_method="nltk_regexp_tokenizer",
    ...     pattern=r"\b[^\d\W]+\b",
    ...     gaps=False,
    ...     num_workers=2
    ... )
    >>> print(tokens)
    [['My', 'name', 'is', 'Dr', 'Jekyll'],
     ['His', 'name', 'is', 'Mr', 'Hyde'],
     ['This', 'guy', 's', 'name', 'is', 'Edward', 'Scissorhands'],
     ['And', 'this', 'is', 'Tom', 'Parker']]
    """
    if not is_string_list(documents):
        raise ValueError("'documents' should be a list of strings")

    return cast(
        NestedTokenList,
        parallelize_func(
            _tokenize_text,
            documents,
            tokenizer_method=tokenizer_method,
            num_workers=num_workers,
            **kwargs,
        ),
    )


def _tokenize_text(
    document: Sentence,
    tokenizer_method: Optional[str] = "nltk_word_tokenizer",
    **kwargs,
) -> TokenList:
    """Tokenize sentence."""
    if tokenizer_method == "nltk_word_tokenizer":  # pragma: no cover
        tokens = nltk.word_tokenize(document, **kwargs)
    elif tokenizer_method == "nltk_regexp_tokenizer":  # pragma: no cover
        tokens = nltk.regexp_tokenize(document, **kwargs)
    return cast(TokenList, tokens)  # pragma: no cover


__all__ = ["batch_tokenize_text"]
