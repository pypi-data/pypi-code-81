#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file contains the utility tool for generating secret keys in django.
# Use the following command for more information:
#
#   $ python -m djangokeys --help
#

import argparse

from djangokeys.secret_key.generate import generate_django_key
from .settings import DJANGO_DEFAULT_KEY_LENGTH


if __name__ == "__main__":

    # build parser object
    parser = argparse.ArgumentParser(
        description="CLI utility tool for generating secret keys in django.",
        prog="python -m djangokeys",
    )

    # first argument is a command
    parser.add_argument(
        'command',
        type=str,
        choices=[
            "generate-key",
            "generate-env",
        ],
        help='specifies which action has to be performed',
    )

    # add length argument
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=DJANGO_DEFAULT_KEY_LENGTH,
        action='store',
        help="changes length of generated key",
    )

    # process command
    parsed = parser.parse_args()
    if parsed.command == "generate-key":
        print(generate_django_key(key_length=parsed.length))
    elif parsed.command == "generate-env":
        print("sorry, this functionality hasn't been implemented yet")
    else:
        print("did not recognize action")
