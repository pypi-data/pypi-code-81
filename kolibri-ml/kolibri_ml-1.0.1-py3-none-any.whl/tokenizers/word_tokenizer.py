
from kolibri.tokenizers.regex_tokenizer import RegexpTokenizer
from kolibri.tokenizers.tokenizer import Tokenizer
from kdmt.text import is_punctuation, is_chinese_char, clean_unicode
from kdmt.dict import update

import unicodedata

tknzr = RegexpTokenizer()

def whitespace_tokenize(text):
    """Runs basic whitespace cleaning and splitting on a piece of text."""
    text = text.strip()
    if not text:
        return []
    tokens = text.split()
    return tokens


class WordTokenizer(Tokenizer):
    name = "word_tokenizer"

    hyperparameters= {
        "fixed": {
            'whitespace': False,
            'regex': None,
            'split_on_punctuation': True
        },

        "tunable": {
        }
    }

    def __init__(self, config={}):
        self.hyperparameters=update(self.hyperparameters, WordTokenizer.hyperparameters)
        super().__init__(config)

        self._tokenize=tknzr.tokenize
        self.do_lower_case=self.get_prameter('do-lower-case')
        if self.get_prameter('whitespace'):
            self._tokenize=whitespace_tokenize
        if self.get_prameter('regex') is not None:
            toknizr=RegexpTokenizer(pattern=self.get_prameter('regex'))
            self._tokenize=toknizr.tokenize
        self.override_default_parameters(config)

    def fit(self, training_data, target):
        return self

    def tokenize(self, text):
        """Tokenizes a piece of text."""

        text = clean_unicode(str(text))

        # This was added on November 1st, 2018 for the multilingual and Chinese
        # models. This is also applied to the English models now, but it doesn't
        # matter since the English models were not trained on any Chinese data
        # and generally don't have any Chinese data in them (there are Chinese
        # characters in the vocabulary because Wikipedia does have some Chinese
        # words in the English Wikipedia.).
        text = self._tokenize_chinese_chars(text)

        orig_tokens = self._tokenize(text)
        split_tokens = []
        for token in orig_tokens:
            if self.do_lower_case:
                token = token.lower()
                token = self._run_strip_accents(token)
            if self.remove_stopwords and token.lower() in self.stopwords:
                continue
            if self.get_prameter('split_on_punctuation'):
                split_tokens.extend(self._run_split_on_punc(token))
            else:
                split_tokens.append(token)


        return split_tokens


    def transform(self, texts, **kwargs):
        return [self.tokenize(d) for d in texts]

    def _run_strip_accents(self, text):
        """Strips accents from a piece of text."""
        text = unicodedata.normalize("NFD", text)
        output = []
        for char in text:
            cat = unicodedata.category(char)
            if cat == "Mn":
                continue
            output.append(char)
        return "".join(output)

    def _run_split_on_punc(self, text):
        """Splits punctuation on a piece of text."""
        chars = list(text)
        i = 0
        start_new_word = True
        output = []
        while i < len(chars):
            char = chars[i]
            if is_punctuation(char):
                output.append([char])
                start_new_word = True
            else:
                if start_new_word:
                    output.append([])
                start_new_word = False
                output[-1].append(char)
            i += 1

        return ["".join(x) for x in output]

    def _tokenize_chinese_chars(self, text):
        """Adds whitespace around any CJK character."""
        output = []
        for char in text:
            cp = ord(char)
            if is_chinese_char(cp):
                output.append(" ")
                output.append(char)
                output.append(" ")
            else:
                output.append(char)
        return "".join(output)

    def get_info(self):
        return "word_tokenizer"


from kolibri.registry import ModulesRegistry
ModulesRegistry.add_module(WordTokenizer.name, WordTokenizer)
