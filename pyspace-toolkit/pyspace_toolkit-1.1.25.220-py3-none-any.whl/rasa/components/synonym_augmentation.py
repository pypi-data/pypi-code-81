
# %%
import re
import os
from typing import Any, Dict, List, Optional, Text, Union, Type

# %%
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.nlu.components import Component
from rasa.nlu.featurizers.featurizer import SparseFeaturizer
from rasa.nlu.training_data import Message, TrainingData

from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES
from rasa.constants import DOCS_URL_TRAINING_DATA_NLU
from rasa.nlu.constants import (
    CLS_TOKEN,
    RESPONSE,
    SPARSE_FEATURE_NAMES,
    TEXT,
    TOKENS_NAMES,
    INTENT,
    MESSAGE_ATTRIBUTES,
    ENTITIES,
)

from rasa.nlu.config import RasaNLUModelConfig

import rasa.utils.io as io_utils
from rasa.nlu import utils
import rasa.utils.common as common_utils
from rasa.nlu.model import Metadata

# %%
from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer

from pyspace.nlp.task.date_extractor import DateParser

# %%
import copy
import pickle

from rasa.core.domain import Domain
from pathlib import Path

import random

class SynonymAugmentation(Component):
    defaults = {
        "minimum_synonym_example_count": 10,
    }

    def __init__(self, component_config: Dict[Text, Any] = None, response_dict=None) -> None:
        super(SynonymAugmentation, self).__init__(component_config)

    def normalize_text(self, text):
        return xNormalizer.tr_normalize(text).lower()

    def get_synonyms(self, training_data):
        
        synonyms = {}
        for key, value in list(training_data.entity_synonyms.items()):
            # key : synonym values # ex: is bankasi
            # value : normalized synonym value # ex: ISCTR

            if key not in synonyms:
                synonyms[key] = set()
            synonyms[key].add(value)

        return synonyms

    def get_pairs(self, training_data):

        synonyms = self.get_synonyms(training_data)

        pairs = {}
        for synonym_key in synonyms:
            pairs[synonym_key] = {}
            pairs[synonym_key]['match_counts'] = {}
            pairs[synonym_key]['match_examples'] = []
            for synonym_i in synonyms[synonym_key]:
                pairs[synonym_key]['match_counts'][synonym_i] = 0

        for synonym_key in synonyms:
            
            for synonym_i in synonyms[synonym_key]:
                synonym_i_norm = self.normalize_text(synonym_i)

                for message in training_data.training_examples:
                    message_text = self.normalize_text(message.text)

                    token_starts = [t.start for t in message.data["tokens"]]
                    token_ends = [t.end for t in message.data["tokens"]]

                    
                    matches = re.finditer(rf'\b{synonym_i_norm}\b', message_text, )
                    for match in matches:
                        match_start, match_end = match.span()

                        if match_start in token_starts and match_end in token_ends:

                            pairs[synonym_key]['match_counts'][synonym_i] += 1
                            pairs[synonym_key]['match_examples'].append( (message, synonym_i, token_starts.index(match_start), token_ends.index(match_end)) )
        return pairs


    def generate_examples(self, training_data):

        augmented_examples = []

        pairs = self.get_pairs(training_data)

        for synonym_key in pairs:
            
            for synonym_i in pairs[synonym_key]['match_counts']:
                synonym_i_train_example_count = pairs[synonym_key]['match_counts'][synonym_i]
                synonym_i_available_augmentation_examples = [match_example for match_example in pairs[synonym_key]['match_examples'] if match_example[1] != synonym_i]
                
                if synonym_i_train_example_count < self.component_config["minimum_synonym_example_count"] :
                    required_example_count = self.component_config["minimum_synonym_example_count"] - synonym_i_train_example_count

                    if required_example_count < len(synonym_i_available_augmentation_examples):
                        synonym_i_available_augmentation_examples = random.sample(synonym_i_available_augmentation_examples, required_example_count)

                    for augmentation_example in synonym_i_available_augmentation_examples:
                        source_message, _ , start_token_index, end_token_index = augmentation_example
                        
                        source_tokens = message.data["tokens"]

                        

                        # TODO only entity control
                        # TODO entity detection 

                        # TODO generate example # augmented_example = Message(text, tokens, entities, lemma)
                    
        return augmented_examples



    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        augmented_examples = self.generate_examples(training_data)
        training_data.training_examples = training_data.training_examples + augmented_examples
        