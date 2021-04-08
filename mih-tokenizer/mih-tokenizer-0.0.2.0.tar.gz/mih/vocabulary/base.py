# encoding: utf-8

import os
import pickle
import numpy as np
import pandas as pd

from pathlib import Path
from typing import List, Union, Tuple, Optional
from collections import OrderedDict
from collections.abc import Iterable

from ..util import logging
logger = logging.getLogger(__name__)

# Define type aliases
Char = str
CharsInput = List[Char]
CharsOutput = CharsInput

Text = str
TextInput = List[Text]

Token = str
TokenInput = List[Token]

Vocab = OrderedDict

# Init default value
IS_CHAR_DEFAULT = True
LOAD_CHARS_DEFAULT = True
VOCAB_FILES_NAMES = {
    "vocab_file": "vocab.txt",
    "chars_file": "chars.pkl",
}


class VocabularyBase:

    def __init__(self, vocab_file=None, **kwargs):
        self.vocab = OrderedDict() if vocab_file is None else self.load_vocab(vocab_file)
        self.special_tokens = []
        self.unk_token = '[UNK]'
        self.add_tokens(self.unk_token, special_tokens=True)

    def __contains__(self, token: Token) -> bool:
        return token in self.vocab

    def __eq__(self, other):
        if isinstance(other, OrderedDict):
            return self.vocab == other
        return self == other

    def items(self):
        return self.vocab.items()

    def is_special(self, token: Token) -> bool:
        return token in self.special_tokens

    @property
    def vocab_size(self):
        return len(self.vocab)

    def add_tokens(self, tokens: Union[Token, TokenInput], special_tokens: bool = False):

        def _add_tokens(token: Token, special_tokens: bool = False):
            if special_tokens and token not in self.special_tokens:
                self.special_tokens.append(token)
            if token not in self.vocab:
                self.vocab[token] = self.vocab_size

        if isinstance(tokens, str):
            _add_tokens(tokens, special_tokens=special_tokens)
            logger.debug(f'vocab size: {self.vocab_size}')
        elif isinstance(tokens, (list, tuple, Iterable, np.ndarray, pd.Series)):
            for token in tokens:
                _add_tokens(token, special_tokens=special_tokens)
            logger.debug(f'vocab size: {self.vocab_size}')
        else:
            raise ValueError(
                f"type of tokens unknown: {type(tokens)}. "
                f"Should be one of a str, list, tuple, set, Iterable, np.ndarray or pd.Series."
            )   

    def create_vocab(self, texts_or_path: Union[List[CharsInput], TextInput, os.PathLike], **kwargs):
        # TODO: support from counter

        is_char = kwargs.get('is_char', IS_CHAR_DEFAULT)

        def _create_vocab_with_special(texts: Union[List[CharsInput], TextInput], **kwargs):
            if is_char:
                self._create_vocab(texts, **kwargs)
            else:
                new_texts = []
                for text in texts:
                    if isinstance(text, str):
                        new_texts.append(text)
                    elif isinstance(text, (list, tuple, np.ndarray, pd.Series)):
                        for t in text:
                            if not self.is_special(t):
                                new_texts.append(t)
                    else:
                        raise ValueError(
                            f"type of text unknown: {type(text)}. "
                            f"Should be one of a str, list, tuple, np.ndarray, pd.Series."
                        )   
                self._create_vocab(new_texts, **kwargs)

        def _create_vocab_byfile(p, **kwargs):
            # TODO: support by kwargs
            # with p.open() as f:
            #     texts = f.readlines()
            with p.open('rb') as f:
                texts = pickle.load(f)
            _create_vocab_with_special(texts, **kwargs)

        def _create_vocab_bydir(p, **kwargs):
            # TODO: support by kwargs
            texts = []
            for _ in p.iterdir():
                with _.open('rb') as f:
                    texts.extend(pickle.load(f))
            _create_vocab_with_special(texts, **kwargs)

        if isinstance(texts_or_path, (list, tuple, np.ndarray, pd.Series)):
            _create_vocab_with_special(texts_or_path, **kwargs)
        else:
            p = Path(texts_or_path)
            if p.is_file():
                _create_vocab_byfile(p, **kwargs)
            elif p.is_dir():
                # TODO:
                # for _ in p.iterdir(): _create_vocab_byfile(_, **kwargs)
                _create_vocab_bydir(p, **kwargs)
            else:
                raise ValueError(
                    f"type of texts_or_path unknown: {type(texts_or_path)}. "
                    f"Should be one of a str, list, tuple, np.ndarray, pd.Series, os.PathLike."
                )   

    def _create_vocab(self, texts: Union[List[CharsInput], TextInput], **kwargs):
        raise NotImplementedError

    def save_vocabulary(
        self,
        save_directory: str,
        filename_prefix: Optional[str] = None,
        chars: Optional[list] = None
    ) -> Tuple[str]:
        index = 0
        os.makedirs(save_directory, exist_ok=True)
        vocab_file = os.path.join(
            save_directory, (filename_prefix + "-" if filename_prefix else "") + VOCAB_FILES_NAMES["vocab_file"]
        )
        with open(vocab_file, "w", encoding="utf-8") as writer:
            for token, token_index in self.vocab.items():
                if index != token_index:
                    logger.warning(
                        "Saving vocabulary to {}: vocabulary indices are not consecutive."
                        " Please check that the vocabulary is not corrupted!".format(vocab_file)
                    )
                    index = token_index
                writer.write(token + "\n")
                index += 1
        chars_file = os.path.join(
            save_directory, (filename_prefix + "-" if filename_prefix else "") + VOCAB_FILES_NAMES["chars_file"]
        )
        with open(chars_file, 'wb') as f:
            pickle.dump(chars, f)
        return (vocab_file, chars_file, )

    def load_vocab(self, save_directory: str, filename_prefix: Optional[str] = None, **kwargs) -> Vocab:
        """Loads a vocabulary file into a dictionary."""
        vocab_file = os.path.join(
            save_directory, (filename_prefix + "-" if filename_prefix else "") + VOCAB_FILES_NAMES["vocab_file"]
        )
        with open(vocab_file, "r", encoding="utf-8") as reader:
            tokens = reader.readlines()
        for index, token in enumerate(tokens):
            token = token.rstrip("\n")
            self.vocab[token] = index

        load_chars = kwargs.get('load_chars', LOAD_CHARS_DEFAULT)
        if load_chars:
            chars_file = os.path.join(
                save_directory, (filename_prefix + "-" if filename_prefix else "") + VOCAB_FILES_NAMES["chars_file"]
            )
            try:
                with open(chars_file, 'rb') as f:
                    chars = pickle.load(f)
                return chars
            except:
                pass
