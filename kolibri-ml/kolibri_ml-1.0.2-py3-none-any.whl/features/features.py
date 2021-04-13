import numpy as np

from kolibri.core.component import Component
from kdmt.dict import update

class Features(Component):
    hyperparameters= {
        "fixed": {

            # list of stop words
            "stop-words": None,  # string {'en'}, list, or None (default)
            # limit vocabulary size
            "max-features": 5000,  # int or None

            # if convert all characters to lowercase
            "case-sensitive": True,  # bool
            "use-bigram-model": False,
            "filter-stopwords": True,
        },

        "tunable": {
            "do-lower-case":{
                "description": "If True all text will be converted to lower case",
                "value": True,
                "type": "boolean",
                "values": [True, False],
            },
        }
    }

    def __init__(self, config):
        self.hyperparameters=update(self.hyperparameters, Component.hyperparameters)
        super().__init__(config)
        self.vectorizer = None


