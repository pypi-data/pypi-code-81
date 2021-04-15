# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.

from gensim.models.doc2vec import TaggedDocument

from .line_sentence_iterator import *


class TaggedDocumentIterator:

    def __init__(self, pls_directory):
        self.iterator_count = 0
        self.iterator = LineSentenceIterator(pls_directory)

    def __iter__(self):
        return self

    def __next__(self):
        document = next(self.iterator)
        value = TaggedDocument(document.rstrip("\n").split(), tags = [self.iterator_count])
        self.iterator_count += 1

        return value
