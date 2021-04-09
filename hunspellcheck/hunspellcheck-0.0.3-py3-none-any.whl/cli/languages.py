"""Language option related stuff for hunspellcheck CLI utilities."""

import argparse
import os

from hunspellcheck.hunspell.dictionaries import (
    gen_available_dictionaries_with_langcodes,
    is_valid_dictionary_language,
)


def create_hunspell_valid_dictionary_action(negotiate_languages=True):
    class HunspellDictionaryNegotiatorAction(argparse._AppendAction):
        """This action allows to redirect a language like 'es' or a dictionary
        filepath to a valid language dictionary supported by hunspell.
        """

        def __call__(self, parser, namespace, values, option_string=None):
            if os.path.isfile(values):
                values = values.rstrip(".dic").rstrip(".aff")
            else:
                (
                    is_valid,
                    dictionary_language,
                    available_dictionaries,
                ) = is_valid_dictionary_language(
                    values,
                    negotiate_languages=negotiate_languages,
                )
                if is_valid:
                    values = dictionary_language

                self.choices = (
                    available_dictionaries
                    if not negotiate_languages
                    else list(gen_available_dictionaries_with_langcodes())
                )
                self.choices.append("<dictionary filepath>")

            # check value manually (seems to me like a hack, but it works)
            parser._check_value(self, values)
            super().__call__(parser, namespace, values, option_string=option_string)

    return HunspellDictionaryNegotiatorAction
