# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.

class Tokenizer:

    @classmethod
    def instantiate(cls, tokenizer_property):
        method = tokenizer_property["method"]
        arguments = tokenizer_property["arguments"]

        if method == "mecab":
            from .mecab_tokenizer import MecabTokenizer
            return MecabTokenizer(** arguments)
        elif method == "janome":
            from .janome_tokenizer import JanomeTokenizer
            return JanomeTokenizer(** arguments)
        elif method == "nltk":
            from .nltk_tokenizer import NltkTokenizer
            return NltkTokenizer(** arguments)
        else:
            raise WScraperTokenizerError(f"No such tokenizer {method}.")
