# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.


from janome.tokenizer import Tokenizer


class JanomeTokenizer:

    def __init__(self):
        self.tokenizer = Tokenizer()

    def split(self, sentence):
        return self.tokenizer.tokenize(sentence, wakati = True)
