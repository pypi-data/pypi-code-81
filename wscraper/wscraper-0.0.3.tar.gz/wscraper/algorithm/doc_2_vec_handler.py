# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.

import glob
import os
from gensim.models.doc2vec import Doc2Vec

from ..analysis import *
from ..utility import *
from ..base import *
from ..tokenizer import *
from ..language import *
from .w_scraper_algorithm_error import *
from .tool.logger import *
from .tool.workspace import *
from .tool.tagged_document_iterator import *


class Doc2VecHandler(Logger):

    algorithm_name = "doc2vec"
    model_file_suffix = ".model"

    logger_name = "doc2vec"

    @classmethod
    def build(cls, task_name = None, model_name = None, *, reset = False, config = None):
        if config is None:
            config = Config(task_name)

        algorithm = config.get_parameter(f"model.{model_name}.{'algorithm'}", must = True)
        arguments = config.get_parameter(f"model.{model_name}.{'arguments'}", must = True)

        if algorithm != cls.algorithm_name:
            raise WScraperAlgorithmError(f"Algorithm mismatched. Assumed `{cls.algorithm_name}` but got `{algorithm}`.")

        model_directory = config.make_model_directory()
        model_path = os.path.join(model_directory, model_name + cls.model_file_suffix)

        if not reset and os.path.isfile(model_path):
            cls.log(f"Model {model_name} already exists. Skipping.")
            return

        if "min_count" not in arguments:
            cls.log("Parameter min_count is not set. Value min_count = 1 is set.")
            arguments["min_count"] = 1

        if "workers" not in arguments:
            worker = config.get_worker(must = True)
            cls.log(f"Parameter workers is not set. wscraper config worker = {worker} is set.")
            arguments["workers"] = worker

        tokenizer_property = config.get_tokenizer(must = True)
        tokenizer = Tokenizer.instantiate(tokenizer_property)

        language = Language.get_class(config.get_language(must = True))

        xml_directory = config.get_wikipedia_xml_directory()
        pls_directory = config.make_workspace("pls")

        Workspace.create_path_line_sentences(xml_directory, pls_directory, language, tokenizer, reset = reset)

        cls.log("Creating a doc2vec model.")
        model = cls.create_model(TaggedDocumentIterator(pls_directory), ** arguments)
        model.save(model_path)
        cls.log(f"A doc2vec model was saved to {model_path}.")

    @classmethod
    def create_model(cls, documents, ** arguments):
        return Doc2Vec(documents = documents, ** arguments)

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
        return cls(Doc2Vec.load(path))

    def __init__(self, model):
        self.model = model

    def save(self, path):
        self.model.save(path)

    def save_keyed_vectors(self, path):
        self.model.wv.save(path)
