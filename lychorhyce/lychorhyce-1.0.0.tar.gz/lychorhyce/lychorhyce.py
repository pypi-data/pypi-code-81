#!/usr/bin/env python3

"""
Copyright (c) 2021 Nicola 'teknico' Larosa <coding@teknico.net>
Licensed under GPLv3 only.
"""

import os
from os import path
import sys

from importlib_metadata import version

from jinja2 import (
    Environment,
    FileSystemLoader,
    select_autoescape,
)

import lychorhyce
from lychorhyce.lcr import (
    get_filenames_and_main_title,
    parse_all,
)


VERSION = version("lychorhyce")
TEMPLATE_FILENAME = "lychorhyce.html.j2"


def ask_yes_no(question, default=True):
    """
    Ask a yes/no question via input() and return their answer.

    "question": string shown to the user.
    "default": presumed answer if the user just hits <Enter>.
        It must be True (the default), False or None (meaning
        an answer is required of the user), otherwise raise KeyError.

    Return True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "no": False, "n": False}
    default_choices = {None: "[y/n]: ", True: "[Y/n]: ", False: "[y/N]: "}
    choices = default_choices[default]

    while True:
        choice = input(f"{question} {choices}").lower()
        if default is not None and choice == '':
            return default
        elif choice in valid:
            return valid[choice]
        else:
            print("Please answer with 'yes' or 'no' (or 'y' or 'n').")


def main():
    """
    Read the source file and write an HTML file with the same name.
    """
    USAGE = f"""
  LyChoRhyce: LYrics, CHOrds and RHYthms, version {VERSION}
  Copyright (c) 2021 Nicola 'teknico' Larosa <coding@teknico.net>
  Licensed under GPLv3 only.

  Parse LCR song text files and generate lyrics + chords + rhythm HTML files.

  Pass the LCR filename as the only argument.
    """
    input_fname, output_fname, main_title, is_error = (
        get_filenames_and_main_title(sys.argv[1:]))
    if is_error:
        sys.exit(USAGE)
    # If output_fname already exists, ask the user.
    if path.exists(output_fname):
        if not ask_yes_no(f"  File '{output_fname}' already exists, overwrite?"):
            sys.exit("  Aborting as requested.")
    # Read the source text file.
    try:
        src = open(input_fname)
    except OSError as err:
        sys.exit(repr(err))
    else:
        lines = src.readlines()
        src.close()
    # Parse the source text lines.
    print(f"  Parsing '{input_fname}'...")
    songs, err_msgs = parse_all(lines)
    # Continue even if there are parsing errors.
    if err_msgs:
        print(f"  WARNING: there are parsing errors. The following lines were discarded:")
        for msg in err_msgs:
            print(f"    {msg}")
    # Generate the HTML from the parsed lines.
    print(f"  Generating HTML...")
    env = Environment(
        # The template is searched in the library directory.
        loader=FileSystemLoader(lychorhyce.__path__[0]),
        autoescape=select_autoescape(["html.j2"]),
        line_statement_prefix='#',
        trim_blocks=True,
        lstrip_blocks=True
    )
    template = env.get_template(TEMPLATE_FILENAME)
    html_markup = template.render(
        main_title=main_title, version=VERSION, songs=songs)
    # Write the generated HTML file with the same name as the source file.
    print(f"  Saving '{output_fname}'...")
    with open(output_fname, 'w') as dst:
        dst.writelines(html_markup)


if __name__ == "__main__":
    main()
