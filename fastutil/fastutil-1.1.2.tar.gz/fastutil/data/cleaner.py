import re
from typing import Iterable, Callable, Union
from multiprocessing.pool import Pool

import tqdm
import zhconv
from w3lib.html import remove_tags
import os
import string
from loguru import logger
from zhon import hanzi

CHINESE_PUNCTUATION: str = hanzi.punctuation
ENGLISH_PUNCTUATION: str = string.punctuation
ALL_PUNCTUATION: str = CHINESE_PUNCTUATION + ENGLISH_PUNCTUATION

CHINESE_CHAR = hanzi.characters
ENGLISH_CHAR = string.ascii_letters
ALL_CHAR = CHINESE_CHAR + ENGLISH_CHAR
DIGITS = string.digits


def get_max_workers(max_workers: Union[str, int]) -> int:
    """接受 "all" 或大于 1 的整数，如果为 "all" 则返回机器的全部 cpu 数量"""
    if isinstance(max_workers, str):
        if max_workers != "all":
            raise ValueError("max_workers only accept string: 'all' ")
        else:
            if os.cpu_count():
                max_workers = os.cpu_count()
            else:
                max_workers = 1
                logger.warning("can not get cpu count, use max_workers=1")
    elif isinstance(max_workers, int):
        if max_workers < 1:
            raise ValueError("Number of max_workers must be at least 1")
        else:
            max_workers = max_workers
    else:
        raise TypeError("Your max_workers is not str or int")

    return max_workers


class BaseCleaner(object):
    def __init__(self, max_workers: int = 1, use_tqdm=True):
        """
        ``Cleaner`` 的抽象基类，需要实现 _clean() 方法

        Parameters
        ----------
        max_workers :
        use_tqdm :
        """
        self.max_workers = get_max_workers(max_workers)
        self.use_tqdm = use_tqdm

    def clean(self, sentence: str) -> str:
        if not isinstance(sentence, str):
            raise TypeError(
                "Cleaner can only clean type str, {} found!".format(type(sentence))
            )

        sentence = sentence.strip()
        if not sentence:
            return ""
        else:
            return self._clean(sentence)

    def _clean(self, sentence):
        raise NotImplementedError

    def clean_sentences(self, sentences: Iterable[str]) -> Iterable[str]:
        """
        clean the collections of sentence. when max_workers != 1, function will call with multiprocessing.
        :param sentences: the collections of sentence, a iterable
        """
        if self.use_tqdm:
            sentences = tqdm.tqdm(sentences)

        if self.max_workers > 1:
            with Pool(processes=self.max_workers) as executor:
                for cleaned_sentence in executor.map(self.clean, sentences):
                    yield cleaned_sentence
        else:
            for sentence in sentences:
                cleaned_sentence = self.clean(sentence)
                yield cleaned_sentence


class HtmlCleaner(BaseCleaner):
    def __init__(self, max_workers=1, which_ones=(), keep=(), encoding=None):
        super().__init__(max_workers=max_workers)
        self.which_ones = which_ones
        self.keep = keep
        self.encoding = encoding

    def _clean(self, sentence: str):
        return remove_tags(
            sentence, which_ones=self.which_ones, keep=self.keep, encoding=self.encoding
        )


class UnexpectedCharCleaner(BaseCleaner):
    def __init__(self, max_workers=1, clean_enter=True):
        super().__init__(max_workers=max_workers)
        self.remain_chars = ALL_CHAR + ALL_PUNCTUATION + DIGITS + " "
        if clean_enter:
            self.remain_chars += "\n"
        clean_chars = r"[^%s]" % self.remain_chars
        self.clean_char_re = re.compile(clean_chars)

    def _clean(self, sentence: str):
        return self.clean_char_re.sub(repl="", string=sentence)


class ErrorPunctuationCleaner(BaseCleaner):
    def __init__(self, max_workers=1):
        super().__init__(max_workers=max_workers)
        self.start_kh_regex = re.compile(r"^[）＞］｝｠｣〉》」』】〕\]+〗〙〛)>}]")
        self.end_kh_regex = re.compile(r"[（＜［｛｟｢〈《「『【〔〖〘〚(<[{]+$")

    def _clean(self, sentence: str):
        sentence = self.start_kh_regex.sub("", sentence)
        sentence = self.end_kh_regex.sub("", sentence)
        return sentence


class GeneralCleaner(BaseCleaner):
    def __init__(
            self, max_workers=1, additional_clean_funcs: Iterable[Callable] = None
    ):
        super().__init__(max_workers=max_workers)
        self.additional_clean_funcs = additional_clean_funcs
        self.html_cleaner = HtmlCleaner()
        self.error_punc_cleaner = ErrorPunctuationCleaner()
        self.unexpected_char_cleaner = UnexpectedCharCleaner()
        self.cleaners = [
            self.html_cleaner,
            self.error_punc_cleaner,
            self.unexpected_char_cleaner,
        ]
        self._blank_re = re.compile(r"\s+")
        self.clean_funcs = [self._convert]

        if additional_clean_funcs:
            self.clean_funcs = self.clean_funcs + list(additional_clean_funcs)

    @staticmethod
    def _convert(sentence):
        return zhconv.convert(sentence, "zh-cn")

    def _clean(self, sentence: str):
        sentence = sentence.replace("\t", " ")
        sentence = self._blank_re.sub(" ", sentence)
        sentence = sentence.strip()

        for cleaner in self.cleaners:
            sentence = cleaner.clean(sentence)

        for clean_fun in self.clean_funcs:
            sentence = clean_fun(sentence)

        return sentence
