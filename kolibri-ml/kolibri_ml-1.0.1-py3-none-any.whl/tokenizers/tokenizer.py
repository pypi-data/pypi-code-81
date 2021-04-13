"""
Tokenizer Interface
"""

from kolibri.core.component import Component
from kolibri.stopwords import get_stop_words
from kdmt.dict import update

class Tokenizer(Component):
    provides = ["tokens"]

    hyperparameters= {
        "fixed": {
            "filter-stopwords": False,
            "language": 'en',
            "do-lower-case": False,
            "custom-stopwords": None,
            "add-to-stopwords": None,
            "remove-from-stopwords": None
        },

        "tunable": {
        }
    }

    def __init__(self, config={}):
        self.hyperparameters=update(self.hyperparameters, Component.hyperparameters)
        super().__init__(config)
        self.stopwords = None
        self.remove_stopwords = self.get_prameter("filter-stopwords")
        if self.remove_stopwords:
            self.stopwords = set(get_stop_words(self.get_prameter('language')))
            if isinstance(self.hyperparameters["add-to-stopwords"], list):
                self.stopwords = list(self.stopwords)
                self.stopwords.extend(list(self.get_prameter("add-to-stopwords")))
                self.stopwords = set(self.stopwords)
            if isinstance(self.get_prameter("remove-from-stopwords"), list):
                self.stopwords = set(
                    [sw for sw in list(self.stopwords) if sw not in self.get_prameter("remove-from-stopwords")])
        if isinstance(self.get_prameter("custom-stopwords"), list):
            self.stopwords = set(self.get_prameter("custom-stopwords"))
        self.tokenizer = None

    def tokenize(self, text):
        raise NotImplementedError
