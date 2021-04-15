import os
import time
from typing import Any, Dict, Text

import joblib
from kolibri.config import ModelConfig
from sklearn.feature_extraction.text import TfidfVectorizer
from kdmt.dict import update
from kolibri.features.features import Features
from kolibri.logger import get_logger
from kolibri.stopwords import get_stop_words

logger = get_logger(__name__)


class TFIDFFeaturizer(Features):
    """Bag of words featurizer

    Creates bag-of-words representation of intent features
    using sklearn's `CountVectorizer`.
    All tokens which consist only of digits (e.g. 123 and 99
    but not ab12d) will be represented by a single feature."""

    name = "tf_idf_featurizer"

    provides = ["text_features"]

    requires = ["tokens"]

    hyperparameters= {
        "fixed": {

            # regular expression for tokens
            "token-pattern": r'(?u)\b\w\w+\b',

            # remove accents during the preprocessing step
            "strip-accents": None,  # {'ascii', 'unicode', None}

            "min-ngram": 1,  # int
        },

        "tunable": {

            "min-df":{
                "description": "min document frequency of a word to add to vocabulary. If float - the parameter represents a proportion of documents. If integer - absolute counts",
                "value": 7,
                "type": "float",
                "range": [0, 0.4]
            },
            "max-df":{
                "description": "max document frequency of a word to add to vocabulary. If float - the parameter represents a proportion of documents. If integer - absolute counts",
                "value": 0.7,
                "type": "float",
                "range": [0.6, 1]
            },

            "max-ngram":{
                "description": "set min)range of ngrams to be extracted",
                "value": 1,
                "type": "integer",
                "range": [1, 3]
            },

        }
    }

    @classmethod
    def required_packages(cls):
        return ["sklearn"]

    def _load_count_vect_params(self):
        # regular expression for tokens
        self.token_pattern = self.get_prameter('token-pattern')

        # remove accents during the preprocessing step
        self.strip_accents = self.get_prameter('strip-accents')

        self.stop_words = None
        # list of stop words
        if self.get_prameter('stop-words'):
            self.stop_words = self.get_prameter('stop-words')
        elif self.get_prameter("filter-stopwords") and self.get_prameter('language'):
            self.stop_words=get_stop_words(self.get_prameter('language'))
        elif self.get_prameter("filter-stopwords") and not self.get_prameter('language'):
            raise Exception('Please specify "language" if you want to remove stop words')

        # min number of word occurancies in the document to add to vocabulary
        self.min_df = self.get_prameter('min-df')

        # max number (fraction if float) of word occurancies
        # in the document to add to vocabulary
        self.max_df = self.get_prameter('max-df')

        # set ngram range
        self.min_ngram = self.get_prameter('min-ngram')
        self.max_ngram = self.get_prameter('max-ngram')

        # limit vocabulary size
        self.max_features = self.get_prameter('max-features')

        # if convert all characters to lowercase
        self.lowercase = self.get_prameter('do-lower-case')

    def __init__(self, hyperparameters=None):
        """Construct a new count vectorizer using the sklearn framework."""
        self.hyperparameters=update(self.hyperparameters, Features.hyperparameters)
        super(TFIDFFeaturizer, self).__init__(hyperparameters)
        if isinstance(hyperparameters, ModelConfig):
            self.override_default_parameters(hyperparameters.as_dict())
        elif isinstance(hyperparameters, dict):
            self.hyperparameters = hyperparameters
        else:
            raise ValueError("Expecting dictionnary or model config, got "+str(type(hyperparameters)))

        # parameters for sklearn's CountVectorizer
        self._load_count_vect_params()

        self.use_bigram_model = self.get_prameter("use-bigram-model")

        self.vectorizer = TfidfVectorizer(min_df=self.min_df, sublinear_tf=True, max_df=self.max_df,
                                          tokenizer=self._identity_tokenizer, lowercase=False,
                                          stop_words=self.stop_words)

    def _identity_tokenizer(self, text):
        return text

    def fit(self, X, y):

        self.vectorizer.fit(X, y)
        return self

    def transform(self, X):

        if self.vectorizer is None:
            logger.error("There is no trained CountVectorizer: "
                         "component is either not trained or "
                         "didn't receive enough training texts")
        else:
            return self.vectorizer.transform(raw_documents=X)

    def train(self, training_data, **kwargs):
        """Take parameters from config and
                construct a new tfidf vectorizer using the sklearn framework."""

        self.vectorizer.fit([doc.tokens for doc in training_data])
        [self.process(doc) for doc in training_data]

    def process(self, document, **kwargs):

        document.vector = self.vectorizer.transform([document.tokens])[0]

    def persist(self, model_dir):
        # type: (Text) -> Dict[Text, Any]
        """Persist this model into the passed directory.
        Returns the metadata necessary to load the model again."""

        featurizer_file = os.path.join(model_dir, self.name + ".pkl")
        joblib.dump(self, featurizer_file)
        return {"featurizer_file": self.name + ".pkl"}

    @classmethod
    def load(cls,
             model_dir=None, model_metadata=None, cached_component=None, **kwargs):

        meta = model_metadata.for_component(cls.name)

        if model_dir and meta.get("featurizer_file"):
            file_name = meta.get("featurizer_file")
            featurizer_file = os.path.join(model_dir, file_name)
            return joblib.load(featurizer_file)
        else:
            logger.warning("Failed to load featurizer. Maybe path {} "
                           "doesn't exist".format(os.path.abspath(model_dir)))
            return TFIDFFeaturizer(meta)

from kolibri.registry import ModulesRegistry
ModulesRegistry.add_module(TFIDFFeaturizer.name, TFIDFFeaturizer)
