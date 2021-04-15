# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.

import pickle

from ..analysis import *
from ..language import *
from ..tokenizer import *
from .tool.logger import *
from .w_scraper_algorithm_error import *


class WordFrequency(Logger):

    algorithm_name = "word_frequency"
    model_file_suffix = ".model"

    logger_name = "word_frequency"

    @classmethod
    def build(cls, task_name = None, model_name = None, *, reset = False, config = None):
        if config is None:
            config = Config(task_nmae)

        algorithm = config.get_parameter(f"model.{model_name}.{'algorithm'}", must = True)
        arguments = config.get_parameter(f"model.{model_name}.{'arguments'}", must = True)

        if algorithm != cls.algorithm_name:
            raise ValueError(f"Algorithm mismatched. Assumed `{algorithm_name}` but got `{algorithm}`.")

        model_directory = config.make_model_directory()
        model_path = os.path.join(model_directory, model_name + cls.model_file_suffix)

        if not reset and os.path.isfile(model_path):
            cls.log(f"Model {model_name} already exists. Skipping.")
            return

        xml_directory = config.get_wikipedia_xml_directory()

        tokenizer_property = config.get_tokenizer(must = True)
        tokenizer = Tokenizer.instantiate(tokenizer_property)

        language = Language.get_class(config.get_language(must = True))

        cls.log("Building word_frequency model...")
        instance = cls.create_count_map(language = language, tokenizer = tokenizer, xml_directory = xml_directory)
        cls.log("Done.")

        instance.save(model_path)
        cls.log(f"Saved to {model_path}.")

    @classmethod
    def create_count_map(cls, language, tokenizer, xml_directory):
        document_frequency = {}
        frequency = {}

        pager = PageIterator(xml_directory)

        with ProgressManager(pager) as progress:
            for page in pager:
                progress.update()

                entry = Parser.page_to_class(page, language = language, entry_only = True)

                if entry is None:
                    continue

                words = []

                for sentence in Parser.to_sentences(entry["mediawiki"], language = language):
                    for word in tokenizer.split(sentence):
                        words.append(word)

                        if word not in frequency:
                            frequency[word] = 1
                        else:
                            frequency[word] += 1

                for word in set(words):
                    if word not in document_frequency:
                        document_frequency[word] = 1
                    else:
                        document_frequency[word] += 1

        return cls({ key: (frequency[key], document_frequency[key]) for key in frequency })

    @classmethod
    def load_from_config(cls, task_name = None, model_name = None, *, config = None):
        if config is None:
            config = Config(task_name)

        algorithm = config.get_parameter(f"model.{model_name}.{'algorithm'}", must = True)

        if algorithm != cls.algorithm_name:
            raise WScraperAlgorithmError(f"Algorithm mismatched. Assumed `{cls.algorithm_name}` but got `{algorithm}`.")

        model_directory = config.make_model_directory()
        model_path = os.path.join(model_directory, model_name + cls.model_file_suffix)

        return cls.load(model_path)

    @classmethod
    def load(cls, path):
        with open(path, "rb") as f:
            model = pickle.load(f)
            return cls(model)

    def __init__(self, model):
        self.model = model

    def save(self, path):
        with open(path, "wb") as f:
            pickle.dump(self.model, f)

    def get_frequency(self, word):
        x = self.model.get(word)

        if x is None:
            return 0

        return x[0]

    def get_document_frequency(self, word):
        x = self.model.get(word)

        if x is None:
            return 0

        return x[1]
