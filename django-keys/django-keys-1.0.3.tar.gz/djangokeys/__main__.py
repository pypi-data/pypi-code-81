#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains script to use tools that are made available by djangokeys package.
# Use the following command for more information:
#
#   $ python -m djangokeys --help
#

if __name__ == "__main__":

    import argparse
    import sys

    from djangokeys.core.generate import generate_django_key
    from djangokeys.settings import DJANGO_DEFAULT_KEY_LENGTH

    # build parser object
    parser = argparse.ArgumentParser(
        description="CLI tool for using djangokeys package.",
        prog="python -m djangokeys",
    )

    # first positional argument is a command
    parser.add_argument(
        'action',
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

    # process action
    parsed = parser.parse_args()
    if parsed.action == "generate-key":
        print(generate_django_key(key_length=parsed.length))
        exit(0)
    else:
        print("This action hasn't been implemented yet!", file=sys.stderr)
        exit(1)
