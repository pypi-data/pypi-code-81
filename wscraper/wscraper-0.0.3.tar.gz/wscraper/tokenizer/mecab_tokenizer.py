# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.


import MeCab


class MecabTokenizer:

    def __init__(self, **kwargs):
        self.tagger = MeCab.Tagger(**kwargs)

    def split(self, sentence):
        words = []

        node = self.tagger.parseToNode(sentence)

        while node:
            word = node.surface
            if len(word) > 0:
                words.append(word)
            node = node.next

        return words
