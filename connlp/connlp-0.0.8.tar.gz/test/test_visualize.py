#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Configuration
import os
import sys

sys.path.append(os.getcwd())
from connlp.preprocess import EnglishTokenizer
from connlp.visualize import Visualizer


## Visualize
# Word Network
def test_word_network(docs):
    tokenizer = EnglishTokenizer()
    tokenized_docs = []
    for sent in docs:
        tokenized_sent = tokenizer.tokenize(text=sent)
        tokenized_docs.append(tokenized_sent)

    visualizer = Visualizer()
    visualizer.network(docs=tokenized_docs, show=True)


## Run
if __name__ == '__main__':
    docs = ['I am a boy', 'She is a girl']
    test_word_network(docs=docs)