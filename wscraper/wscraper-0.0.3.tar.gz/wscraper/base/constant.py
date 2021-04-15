# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.


import os


class Constant:

    root_directory = os.environ.get("WSCRAPER_ROOT") or os.path.join(os.environ["HOME"], ".wscraper")

    root_config = os.path.join(root_directory, "config.yml")
    root_status = os.path.join(root_directory, "status.yml")

    task_directory = os.path.join(root_directory, "task")
    wikipedia_directory = os.path.join(root_directory, "wikipedia")

    available_languages = [
        "japanese",
        "english"
    ]

    available_algorithms = [
        "word2vec",
        "doc2vec",
        "word_frequency"
    ]

    available_tokenizers = [
        "mecab",
        "janome",
        "nltk"
    ]

    min_page_chunk = 100
    max_page_chunk = 10 ** 7
    min_worker = 1
    max_worker = 64
