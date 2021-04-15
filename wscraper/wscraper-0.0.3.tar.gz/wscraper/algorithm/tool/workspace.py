# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.

import sys

from ...utility import *
from ...analysis import *
from .logger import *


class Workspace(Logger):

    logger_name = "workspace"

    @classmethod
    def create_path_line_sentences(cls, xml_directory, pls_directory, language, tokenizer, *, reset = False):
        existing_files = glob.glob(os.path.join(pls_directory, "*.txt"))

        if len(existing_files) > 0:
            if not reset:
                cls.log(f"Path line sentences already exist at {pls_directory}. Skipping.")
                return
            else:
                cls.log(f"Path line sentences exist at {pls_directory}. Removing.")
                for path in existing_files:
                    os.remove(path)
                cls.log("Existing files were removed.")

        cls.log("Creating path line sentences...")

        pager = PageIterator(xml_directory)
        writer = FileWriter(pls_directory, "{:06d}.txt", 10000)
        progress = ProgressManager(writer)

        with writer, progress:
            for page in pager:
                progress.update()

                entry = Parser.page_to_class(page, language = language, entry_only = True)

                if entry is None:
                    continue

                plain_text = Parser.to_plain_text(entry["mediawiki"], language = language)
                plain_text = plain_text.replace("\n", " ").strip()

                line = " ".join(tokenizer.split(plain_text))

                writer.write(line + "\n")

        cls.log("Done!")
