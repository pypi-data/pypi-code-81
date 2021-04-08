# encoding: utf-8

import numpy as np
import pandas as pd

from enum import Enum
from itertools import chain
from pathlib import Path
from collections import Counter
from typing import List, Dict, Union, Tuple, Optional

from ...vocabulary import VocabularyBase
from ...tokenizer import TokenizerBase


# Define type aliases
Vocabulary = VocabularyBase


class MethodSupport(Enum):

    MOST_FREQ_1 = 'most_freq_1'
    MOST_FREQ_ALL = 'most_freq_all'

    LESS_FREQ_1 = 'less_freq_1'
    LESS_FREQ_ALL = 'less_freq_all'

    MOST_LESS_FREQ_1 = 'most_less_freq_1'
    MOST_LESS_FREQ_ALL = 'most_less_freq_all'

    TFIDF_1 = 'tfidf_1'
    TFIDF_ALL = 'tfidf_all'


METHOD_MOST_FREQ = [
    MethodSupport.MOST_FREQ_1,
    MethodSupport.MOST_FREQ_ALL,
]

METHOD_LESS_FREQ = [
    MethodSupport.MOST_FREQ_1,
    MethodSupport.MOST_FREQ_ALL,
]

METHOD_MOST_LESS_FREQ = [
    MethodSupport.MOST_LESS_FREQ_1,
    MethodSupport.MOST_LESS_FREQ_ALL,
]

METHOD_FREQ = METHOD_MOST_FREQ + METHOD_LESS_FREQ + METHOD_MOST_LESS_FREQ

METHOD_TFIDF = [
    MethodSupport.TFIDF_1,
    MethodSupport.TFIDF_ALL,
]


class Priority(Enum):
    """
    Not used on METHOD ALL
    """

    MAX_LENGTH_FIRST = 'max_length_first'
    MIN_LENGTH_FIRST = 'min_lenght_first'


# Define type aliases
Char = str
CharsInput = List[Char]
CharsOutput = CharsInput

Token = Char
TokenId = int
TokenInput = List[Token]
TokenOutput = TokenInput

Text = str
TextInput = List[Text]


# Init default value
MAX_LENGTH_DEFAULT = 7
METHOD_DEFAULT = MethodSupport.MOST_FREQ_1
PRIORITY_DEFAULT = Priority.MAX_LENGTH_FIRST

VOCAB_SIZE_DEFAULT = 1e4
KEEP_SINGLE_DEFAULT = True
CONVERT_UNKNOWN_DEFAULT = True
CHECHKPOINT_DEFAULT = None
AUTOSAVE_DEFAULT = True


class BPE:

    def to_char(self, texts: Union[Text, TextInput, List[CharsInput]]) -> Union[CharsInput, List[CharsInput]]:
        # TODO: about space and control
        # TODO: implement by normalizer
        return texts

    def to_pairs(self, chars: Union[Text, CharsInput, List[CharsInput]], **kwargs) -> Union[CharsOutput, List[CharsOutput]]:
        """
        Get all possible pairs, limit by {max_length}
        """
        if isinstance(chars, str):
            return self._to_pairs(chars)
        elif isinstance(chars, (list, tuple, np.ndarray, pd.Series)):
            first_element = chars[0]
            if isinstance(first_element, (str, list, tuple, np.ndarray, pd.Series)):
                pairs = [self._to_pairs(_) for _ in chars]
                return [_ for _ in pairs if _]
            else:
                raise ValueError(
                    f"type of chars element unknown: {type(first_element)}. "
                    f"Should be one of a str, list, tuple, np.ndarray or pd.Series."
                )
        else:
            raise ValueError(
                f"type of chars unknown: {type(chars)}. "
                f"Should be one of a list, tuple, np.ndarray or pd.Series."
            )

    def _to_pairs(self, chars: Union[Text, CharsInput], **kwargs) -> CharsOutput:
        max_length = kwargs.get('max_length', MAX_LENGTH_DEFAULT)
        if isinstance(chars, str) and 2 >= len(chars):
            return [chars]
        elif 2 > len(chars):
            return []
        else:
            pairs = [chars[i]+chars[i+1] for i in range(len(chars)-1)]
            return [p for p in pairs if max_length >= len(p)]

    def get_pairs(self, chars: Union[CharsInput, List[CharsInput]], **kwargs) -> Union[CharsOutput, List[CharsOutput]]:
        method = kwargs.get('method', METHOD_DEFAULT)

        if method in METHOD_FREQ:
            return self._get_pairs_freq(chars, **kwargs)
        elif method in METHOD_TFIDF:
            return self._get_pairs_tfidf(chars, **kwargs)
        else:
            raise ValueError(
                f"type of method unknown: {method}. "
                f"Should be one of a {METHOD_FREQ} or {METHOD_TFIDF}."
            )

    def _get_pairs_freq(self, chars: Union[CharsInput, List[CharsInput]], **kwargs) -> Union[CharsOutput, List[CharsOutput]]:
        raise NotImplementedError

    def _get_pairs_tfidf(self, chars: Union[CharsInput, List[CharsInput]], **kwargs) -> Union[CharsOutput, List[CharsOutput]]:
        raise NotImplementedError

    def update(
        self,
        chars: Union[Text, TextInput, List[CharsInput]],
        pairs: Union[Char, CharsOutput]
    ) -> Union[CharsOutput, List[CharsOutput]]:
        if isinstance(chars, str):
            return self._update(chars, pairs)
        elif isinstance(chars, (list, tuple, np.ndarray, pd.Series)):
            first_element = chars[0]
            if isinstance(first_element, (str, list, tuple, np.ndarray, pd.Series)):
                return [self._update(_, pairs) for _ in chars]
                # return self._update(chars, pairs)
            else:
                raise ValueError(
                    f"type of chars element unknown: {type(first_element)}. "
                    f"Should be one of a str, list, tuple, np.ndarray or pd.Series."
                )
        else:
            raise ValueError(
                f"type of chars unknown: {type(chars)}. "
                f"Should be one of a list, tuple, np.ndarray or pd.Series."
            )

    def _update(
        self,
        chars: Union[Text, CharsInput],
        pairs: Union[Char, CharsOutput]
    ) -> CharsOutput:

        if 1 >= len(chars):
            return chars
        else:
            if isinstance(chars, str): chars = list(chars)
            if isinstance(pairs, str): pairs = [pairs]
            for pair in pairs:
                new_chars = []
                i = 0
                while(i < len(chars)):
                    if pair == ''.join(chars[i:i+2]):
                        new_chars.append(pair)
                        i += 2
                        continue
                    new_chars.append(chars[i])
                    if i == (len(chars)-2):
                        new_chars.append(chars[i+1])
                        break
                    i += 1
                chars = new_chars
            return chars


class VocabularyBPE(VocabularyBase, BPE):

    def _get_pairs_freq(self, chars: List[CharsInput], **kwargs) -> List[CharsOutput]:
        """
        Get appropriate pair(s) by {method} and {priority}
        """
        method = kwargs.get('method', METHOD_DEFAULT)
        if method in METHOD_MOST_FREQ:
            return self._get_pairs_freq_most(chars, **kwargs)
        elif method in METHOD_LESS_FREQ:
            return self._get_pairs_freq_less(chars, **kwargs)
        elif method in METHOD_MOST_LESS_FREQ:
            return self._get_pairs_freq_most_less(chars, **kwargs)
        else:
            raise ValueError(
                f"type of method unknown: {method}. "
                f"Should be one of a {METHOD_FREQ}."
            )

    def _get_pairs_freq_most(self, chars: List[CharsInput], **kwargs) -> List[CharsOutput]:
        method = kwargs.get('method', METHOD_DEFAULT)
        if MethodSupport.MOST_FREQ_1 == method:
            return self._get_pairs_freq_most_1(chars, **kwargs)
        elif MethodSupport.MOST_FREQ_ALL == method:
            return self._get_pairs_freq_most_all(chars, **kwargs)
        else:
            raise ValueError(
                f"type of method unknown: {method}. "
                f"Should be one of a {MethodSupport.MOST_FREQ}."
            )

    def _get_pairs_freq_most_1(self, chars: List[CharsInput], **kwargs) -> List[CharsOutput]:
        return self._get_pairs_freq_most_all(chars)[0]

    def _get_pairs_freq_most_all(self, chars: List[CharsInput], **kwargs) -> List[CharsOutput]:
        counter = Counter(chain.from_iterable(chars))

        most_freq = counter.most_common(1)[0][1]
        pairs = []
        for (k, cnt) in  counter.most_common():
            if most_freq == cnt:
                pairs.append(k)
                continue
            break

        return self._order_pairs(pairs)

    def _get_pairs_freq_less(self, chars: List[CharsInput], **kwargs) -> List[CharsOutput]:
        # TODO:
        raise NotImplementedError

    def _get_pairs_freq_most_less(self, chars: List[CharsInput], **kwargs) -> List[CharsOutput]:
        # TODO:
        raise NotImplementedError

    def _get_pairs_tfidf(self, chars: List[CharsInput], **kwargs) -> List[CharsOutput]:
        """
        Get appropriate pair(s) by {method} and {priority}
        """
        # TODO:
        raise NotImplementedError

    def _order_pairs(self, pairs: CharsInput, **kwargs) -> CharsOutput:
        priority = kwargs.get('priority', PRIORITY_DEFAULT)
        
        if Priority.MAX_LENGTH_FIRST == priority:
            return sorted(pairs, key=len, reverse=True)
        elif Priority.MIN_LENGTH_FIRST == priority:
            return sorted(pairs, key=len)
        else:
            raise ValueError(
                f"type of priority unknown: {priority}. "
                f"Should be one of a {Priority.MAX_LENGTH_FIRST} or {Priority.MIN_LENGTH_FIRST}."
            )

    def _create_vocab(self, texts: Union[List[CharsInput], TextInput], **kwargs):
        vocab_size = kwargs.get('vocab_size', VOCAB_SIZE_DEFAULT)
        keep_single = kwargs.get('keep_single', KEEP_SINGLE_DEFAULT)
        checkpoint = kwargs.get('checkpoint', CHECHKPOINT_DEFAULT)
        autosave = kwargs.get('autosave', AUTOSAVE_DEFAULT)

        chars = self.to_char(texts)

        if keep_single:
            self.add_tokens(sorted(list(set(chain.from_iterable(chars)))))

        while(self.vocab_size < vocab_size):
            pairs = self.to_pairs(chars)
            if not pairs: break
            pairs = self.get_pairs(pairs, **kwargs)
            self.add_tokens(pairs)
            chars = self.update(chars, pairs)
            if checkpoint and 0 == self.vocab_size % checkpoint:
                self.save_vocabulary('./.vocab/.checkpoint-%s' % self.vocab_size, chars=chars)
        self.save_vocabulary('./.vocab/.checkpoint-last', chars=chars)


class TokenizerBPE(TokenizerBase, BPE):

    def __init__(self, vocab: Vocabulary=None, **kwargs):
        self.vocab = vocab
        super().__init__(**kwargs)

    def _get_pairs(self, chars: CharsInput, **kwargs) -> CharsOutput:
        method = kwargs.get('method', METHOD_DEFAULT)

        if (isinstance(method,MethodSupport) and method.value.endswith('1')) or (isinstance(method,str) and method.endswith('1')):
            for k, _ in self.vocab.items():
                if k in chars:
                    return k
            return ''

        return [k for k, _ in self.vocab.items() if k in chars]

    def _get_pairs_freq(self, chars: CharsInput, **kwargs) -> CharsOutput:
        """
        Get appropriate pair(s) by {method} and {priority} with importance of vocab order.
        """
        return self._get_pairs(chars, **kwargs)

    def _get_pairs_tfidf(self, chars: CharsInput, **kwargs) -> CharsOutput:
        """
        Get appropriate pair(s) by {method} and {priority} with importance of vocab order.
        """
        return self._get_pairs(chars, **kwargs)

    def _tokenize(self, texts: Union[Text, CharsInput], **kwargs) -> CharsOutput:
        """
        Split a string into char, then merge pair char by ordered vocab until no more find.
        Replacing unknown tokens with the :obj:`unk_token`.
        """
        convert_unknown = kwargs.get('convert_unknown', CONVERT_UNKNOWN_DEFAULT)

        def merge(chars: Union[Text, CharsInput], **kwargs) -> CharsOutput:
            """
            Merge pair char by ordered vocab.
            """
            need_merge = True
            while(need_merge):
                need_merge, chars = _merge(chars, **kwargs)
            return chars

        def _merge(chars: Union[Text, CharsInput], **kwargs) -> CharsOutput:
            """
            Use trained vocabulary makes it different from get_pairs().
            The importance of Token has already been recorded by vocab order.
            """
            pairs = [c for c in self._to_pairs(chars, **kwargs) if c in self.vocab]
            if not pairs: return False, chars

            pairs = self.get_pairs(pairs)
            chars = self._update(chars, pairs)
            return True, chars

        def to_unknown(chars: Union[Text, CharsInput], vocab: Vocabulary):
            # TODO: to be implement with transformers
            return [c if c in self.vocab else self.vocab.unk_token for c in chars]

        chars = self.to_char(texts)
        chars = merge(chars)
        if convert_unknown:
            chars = to_unknown(chars, self.vocab)
        return chars
