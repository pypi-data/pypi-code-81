from kolibri.tokenizers.tokenizer import Tokenizer
from kdmt.text import split_tet_to_sentences
from kdmt.dict import update

class SentenceTokenizer(Tokenizer):
    name = "sentence_tokenizer"

    provides = ["sentences"]

    hyperparameters= {
        "fixed": {
        },

        "tunable": {
            "split-on-new-line": {
                "value": True,
                "type": "categorical",
                "values": [True, False]
            }
        }
    }

    def __init__(self, config={}):
        self.hyperparameters=update(self.hyperparameters, Tokenizer.hyperparameters)
        super().__init__(config)

        self.override_default_parameters(config)

        self.split_on_new_line=self.get_prameter("split-on-new-line")

    def tokenize(self, text):
        sentences = split_tet_to_sentences(text, self.split_on_new_line)

        return [sent.strip() for sent in sentences if len(sent.strip()) > 0]

    def transform(self, X):
        return [self.tokenize(x) for x in X]


from kolibri.registry import ModulesRegistry
ModulesRegistry.add_module(SentenceTokenizer.name, SentenceTokenizer)

