#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file contains the utility tool for generating secret keys in django.
# Use the following command for more information:
#
#   $ python -m djangokeys --help
#

import argparse

from .generate import generate_django_key
from .settings import DJANGO_DEFAULT_KEY_LENGTH


class GenerateKeyAction(argparse.Action):
    """ Handles environment created by the parser to generate key.
    """

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(GenerateKeyAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print(generate_django_key(key_length=values))


if __name__ == "__main__":

    # build parser object
    parser = argparse.ArgumentParser(
        description="CLI utility tool for generating secret keys in django.",
        prog="python -m djangokeys",
    )

    # add length argument
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=DJANGO_DEFAULT_KEY_LENGTH,
        action=GenerateKeyAction,
        help="changes length of generated key (default: {})".format(
            DJANGO_DEFAULT_KEY_LENGTH),
    )

    # process command
    parser.parse_args()
