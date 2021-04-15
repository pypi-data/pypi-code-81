from tokenizers import BertWordPieceTokenizer
import jieba_fast as jieba
import spacy
import json
from typing import List


class SocoBertTokenizer(object):
    CHAR = 'char'
    WORD = 'word'
    ALL = "all"
    UNK = '[UNK]'

    def __init__(self, base_vocab_path, final_vocab_path, lang, uncased=True, add_special_tokens=False):
        self._lang = lang
        self._uncased = uncased
        self._add_special_tokens = add_special_tokens
        self._tokenizer = BertWordPieceTokenizer(base_vocab_path,
                                                 handle_chinese_chars=self._lang=='zh',
                                                 lowercase=uncased)
        if self._lang == 'en':
            self.en_spacy = spacy.load('en_core_web_sm')

        elif self._lang == 'zh':
            jieba.initialize()
            self.en_spacy = None
        else:
            raise Exception

        print("Load tokenizer {} - {}".format(base_vocab_path, lang))

        # remove words that are UNK in tokenizer's vocab
        vocab = [w if type(w) is str else tuple(w) for w in json.load(open(final_vocab_path))]
        self._valid_vocab = set(vocab)
        self.vocab2id = {v: idx for idx, v in enumerate(vocab)}
        self.id2vocab = vocab

        print("Load vocab of size (original {}) = {} ".format(self._tokenizer.get_vocab_size(), len(vocab)))

    @property
    def sep_token(self):
        return '[SEP]'

    @property
    def cls_token(self):
        return '[CLS]'

    def _wp_tokenize(self, text) -> List[str]:
        res = self._tokenizer.encode(text, add_special_tokens=self._add_special_tokens).tokens
        return res

    def _word_tokenize(self, text):
        if self._uncased:
            text = text.lower()

        if self._lang == 'en':
            return [(w.text, w.idx, w.idx+len(w)) for w in self.en_spacy(text, disable=["tagger", "parser", "ner"])]

        elif self._lang == 'zh':
            return list(jieba.tokenize(text))
        else:
            raise Exception("Not supported yet")

    def _map_word_to_subword(self, wor_tokens, sub_data):
        results = []
        for w in wor_tokens:
            if w[0] not in set(sub_data):
                results.append(w[0])

        return results

    def _normalize(self, tokens):
        new_results = []
        for t in tokens:
            if t in self._valid_vocab:
                new_results.append(t)

        return new_results

    def _tokenize(self, text, mode=CHAR):
        if mode == self.CHAR:
            results = self._wp_tokenize(text)

        elif mode == self.WORD:
            wor_tokens = self._word_tokenize(text)
            results = []
            for w in wor_tokens:
                sub_tokens = self._wp_tokenize(w[0])
                if len(sub_tokens) > 1 and tuple(sub_tokens) in self._valid_vocab:
                    results.append(tuple(sub_tokens))
                else:
                    results.extend(sub_tokens)

        elif mode == self.ALL:
            sub_res = self._wp_tokenize(text)
            wor_tokens = self._word_tokenize(text)
            new_tokens = self._map_word_to_subword(wor_tokens, sub_res)
            results = sub_res

            for w in new_tokens:
                sub_tokens = self._wp_tokenize(w)
                if len(sub_tokens) > 1 and tuple(sub_tokens) in self._valid_vocab:
                    results.append(tuple(sub_tokens))
        else:
            raise Exception("Not supported yet")

        return results

    def tokenize(self, text, mode=CHAR, normalize=True, max_len=1e10):
        if self._uncased:
            text = text.lower()

        tokens = self._tokenize(text, mode)

        max_len = int(max_len)
        if normalize:
            return self._normalize(tokens)[0:max_len]
        else:
            return tokens[0:max_len]

    def convert_tokens_to_ids(self, tokens):
        q_ids = []
        for token in tokens:
            if type(token) is str:
                q_ids.append(self.vocab2id[token])
            else:
                q_ids.append(self.vocab2id[tuple(token)])

        return q_ids

    def convert_ids_to_tokens(self, ids):
        return [self.id2vocab[id] for id in ids]




