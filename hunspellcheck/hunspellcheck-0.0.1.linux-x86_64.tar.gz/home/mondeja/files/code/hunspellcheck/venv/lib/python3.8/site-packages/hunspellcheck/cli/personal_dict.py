"""Personal dictionary CLI option stuff."""

import argparse
import os


class PersonalDictionaryAction(argparse._StoreAction):
    def __call__(self, parser, namespace, values, option_string=None):
        filename = values[0]
        if not os.path.isfile(filename):
            raise FileNotFoundError(
                f'Personal dictionary file not found at "{filename}"'
            )
        super().__call__(parser, namespace, filename, option_string=option_string)
