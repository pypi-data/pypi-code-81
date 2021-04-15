# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.

import nltk


class NltkTokenizer:

    def __init__(self, **kwargs):
        pass

    def split(self, sentence):
        return nltk.word_tokenize(sentence)
