from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from hmmlearn import hmm
import string
import nltk
import re
from nltk.corpus import words, wordnet
import numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize

from pyhumour._utilities.preprocess import preprocess_text
import math


class HMMHelper:
    """
    HMMHelper class is used for creating the Hidden Markov Model for the corpus given. It also calculates the
    score of any new text sent by the user
    """

    def __init__(self, texts: list):
        """
        self._texts -> the corpus or the dataset given by the user.
        self._tokenizer -> keras tokenizer based on the corpus
        self._hmm_trained -> trained hmm model
        """
        self._texts = texts
        self._tokenizer = self.get_tokenizer(200000)
        self._hmm_trained = self.get_hmm()

    def get_tokenizer(self, max_features: int):
        """
        Training the tokenizer with keras tokenizer method
        """
        tokenizer = Tokenizer(num_words=max_features, oov_token=True)
        tokenizer.fit_on_texts(self._texts)
        return tokenizer

    def get_hmm(self):
        """
        Training the HMM model
        """
        hmm_trained = hmm.GaussianHMM(
            n_components=3, n_iter=50, init_params="mcs")
        sequences = self._tokenizer.texts_to_sequences(self._texts)
        lengths = [len(i) for i in sequences]
        while 0 in lengths:
            sequences.remove(sequences[lengths.index(0)])
            lengths.remove(0)
        sequences = [np.array(i) for i in sequences]
        sequences = [i.reshape(i.shape[0], 1) for i in sequences]
        sequences = np.concatenate(sequences)
        hmm_trained.fit(sequences, lengths)
        return hmm_trained

    def get_hmm_score(self, text):
        """
        Returns the Log probability HMM score for text sent by user.
        """
        text = preprocess_text(text)
        sentence = word_tokenize(text)
        text = ' '.join(sentence)
        X = self._tokenizer.texts_to_sequences([text])
        lengths = [len(i) for i in X]
        X = [np.array(i) for i in X]
        X = [i.reshape(i.shape[0], 1) for i in X]
        values = []
        for i in X:
            if i.shape[0] == 0:
                values.append(0)
            else:
                values.append(self._hmm_trained.score(i))
        if values:
            return values[0]
        else:
            return 0.0


class NgramHelper:
    def __init__(self, texts: list):
        self._texts = texts
        self._golden_vocab = words.words()
        self._golden_vocab = [word.lower() for word in self._golden_vocab]
        self._vocab = set()
        self._unknown = set()
        self._individual_sentences = list()
        self._bigram = dict()
        self._trigram = dict()
        self._special_characters = string.punctuation + \
            "'[@_!#$%^&*()<>?/\|}{~:]'"

    def get_special_characters(self):
        return self._special_characters

    def get_golden_vocab(self):
        return self._golden_vocab

    def get_unknown(self):
        return self._unknown

    def get_individual_sentences(self):
        return self._individual_sentences

    def get_bigrams(self):
        if len(self._individual_sentences) != len(self._texts):
            self.get_vocab()
        for i in range(len(self._individual_sentences)):
            word_list = self._individual_sentences[i]
            if len(word_list) >= 2:
                for j in range(0, len(word_list)-1):
                    if tuple([word_list[j], word_list[j+1]]) not in self._bigram:
                        self._bigram[tuple([word_list[j], word_list[j+1]])] = 1
                    else:
                        self._bigram[tuple(
                            [word_list[j], word_list[j+1]])] += 1
        return self._bigram

    def get_trigrams(self):
        if len(self._individual_sentences) != len(self._texts):
            self.get_vocab()
        for i in range(len(self._individual_sentences)):
            word_list = self._individual_sentences[i]
            if len(word_list) >= 3:
                for j in range(0, len(word_list)-2):
                    if (word_list[j], word_list[j+1], word_list[j+2]) not in self._trigram:
                        self._trigram[(
                            word_list[j], word_list[j+1], word_list[j+2])] = 1
                    else:
                        self._trigram[(
                            word_list[j], word_list[j+1], word_list[j+2])] += 1
        return self._trigram

    def get_vocab(self):
        for i in range(len(self._texts)):
            word_list = self._texts[i].split()
            modified_word_list = []
            for w in word_list:
                if (w in self._golden_vocab) or (w in self._special_characters) or (len(wordnet.synsets(w)) > 0):
                    modified_word_list.append(w)
                    self._vocab.add(w)
                else:
                    self._unknown.add(w)
                    modified_word_list.append("<unk>")
            modified_word_list.insert(0, "<s>")
            modified_word_list.insert(0, "<s>")
            modified_word_list.append("</s>")
            modified_word_list.append("</s>")
            self._individual_sentences.append(modified_word_list)
        return self._vocab

    def get_ngram_score(self, text: str):
        if self._vocab == set():
            self.get_vocab()
        if self._trigram is None:
            self.get_trigrams()
        text = preprocess_text(text)
        sentences = sent_tokenize(text)
        sentence_list = []
        for j in range(len(sentences)):
            sentences[j] = sentences[j].replace("\n", " ")
            word_list = word_tokenize(sentences[j])
            modified_word_list = []
            for word in word_list:
                full_stop = 0
                exclamation = 0
                single_quote = 0
                double_quote = 0
                if word == "''" or word == "``":
                    word = '"'
                if (len(word) > 1) and ("'" in word):
                    if word[0] == "'":
                        modified_word_list.append("'")
                    if word[-1] == "'":
                        single_quote = 1
                    word = word.replace("'", "")
                if (len(word) > 1) and ('"' in word):
                    if word[0] == '"':
                        modified_word_list.append('"')
                    if word[-1] == '"':
                        double_quote = 1
                    word = word.replace('"', "")
                if (len(word) > 1) and ("." in word):
                    c = 0
                    for char in word:
                        if char == ".":
                            c += 1
                    if word[0] == "." and c == 1:
                        modified_word_list.append(".")
                    if word[-1] == "." and c == 1:
                        full_stop = 1
                    word = word.replace(".", "")
                if (len(word) > 1) and ("!" in word):
                    if word[-1] == "!":
                        modified_word_list.append("!")
                    word = word.replace("!", "")
                if (word in self._special_characters) or (len(wordnet.synsets(word)) > 0) or (word in self._golden_vocab):
                    modified_word_list.append(word)
                elif ("." in word) or ("-" in word) or ("/" in word):
                    word = re.sub("[.\-\/]", " ", word)
                    split_words = word.strip().split()
                    for split_word in split_words:
                        modified_word_list.append(split_word)
                else:
                    modified_word_list.append("<unk>")
                if full_stop == 1:
                    modified_word_list.append(".")
                if exclamation == 1:
                    modified_word_list.append("!")
                if single_quote == 1:
                    modified_word_list.append("'")
            modified_word_list.insert(0, "<s>")
            modified_word_list.insert(0, "<s>")
            modified_word_list.append("</s>")
            modified_word_list.append("</s>")
            sentence_list.append(modified_word_list)

        group_probabilities = []
        for sentence in sentence_list:
            word_list = sentence
            probability = 0
            if len(word_list) > 0:
                for j in range(len(word_list) - 2):
                    if (word_list[j], word_list[j + 1], word_list[j + 2]) not in self._trigram:
                        probability += math.log(1 / len(self._vocab))
                    else:
                        probability += math.log(
                            self._trigram[(word_list[j], word_list[j + 1], word_list[j + 2])])
            group_probabilities.append(probability)

        return sum(group_probabilities) / len(group_probabilities)
