import os
import re
from pathlib import Path
from typing import Any

from mdscript.files_dependencies_manager import FilesDependenciesManager
from mdscript.watcher import Watcher


class Runner:
    def __init__(self, config: Any, base_dirpath: str):
        self.config = config
        self.base_dirpath = base_dirpath
        self.watcher = Watcher(runner=self)
        self.files_dependencies = FilesDependenciesManager(watcher=self.watcher)

    def _run_in_file(self, source_filepath: str, output_filepath: str, run_test: bool):
        with open(source_filepath, 'r') as source_markdown_file:
            source_file_content = source_markdown_file.read()

            rendered_file_content = ""
            remaining_unprocessed_file_content = source_file_content

            transformers_names_selectors = '|'.join(self.config.transformers.keys())
            transformers_regex = '({{)' + f'({transformers_names_selectors})' + '(::)(.*)(}})'
            # Instead of looking for each transformer one by one, we create a simple regex tasked with finding any transformer

            for match in re.finditer(pattern=transformers_regex, string=source_file_content):
                match_start = match.start()
                match_end = match.end()

                index_relative_to_remaining_unprocessed = len(source_file_content) - len(remaining_unprocessed_file_content)
                unprocessed_text_pre_match = remaining_unprocessed_file_content[0:match_start - index_relative_to_remaining_unprocessed]
                remaining_unprocessed_file_content = remaining_unprocessed_file_content[match_end - index_relative_to_remaining_unprocessed:]

                transformer_name = match[2]
                transformer_attribute = match[4]
                transformer_class_type = self.config.transformers.get(transformer_name, None)
                if transformer_class_type is None:
                    raise Exception(f"No transformer found for {transformer_name}")

                transformer_instance = transformer_class_type(
                    runner=self, source_filepath=source_filepath, attribute=transformer_attribute
                )
                if run_test is True:
                    transformer_instance.test()

                transformed_content = transformer_instance.transform()
                rendered_file_content += f"{unprocessed_text_pre_match}{transformed_content}"
            rendered_file_content += remaining_unprocessed_file_content

            with open(output_filepath, 'w+') as output_file:
                output_file.write(rendered_file_content)

    def _run_with_filepath(self, source_filepath: str, run_test: bool):
        source_filepath_parts = Path(source_filepath).parts
        output_filepath = os.path.join(*source_filepath_parts[0:len(source_filepath_parts)-1], source_filepath_parts[-1][2:])
        self._run_in_file(source_filepath=source_filepath, output_filepath=output_filepath, run_test=run_test)

    def _run_in_folder(self, dirpath: str, run_tests: bool):
        for root_dirpath, dirs, filenames in os.walk(dirpath):
            for filename in filenames:
                if filename[0:2] == '__':
                    source_filepath = os.path.join(root_dirpath, filename)
                    output_filename = filename[2:]
                    output_filepath = os.path.join(root_dirpath, output_filename)
                    self._run_in_file(source_filepath=source_filepath, output_filepath=output_filepath, run_test=run_tests)

    def _start(self, run_tests: bool):
        self._run_in_folder(dirpath=self.base_dirpath, run_tests=run_tests)
        # When starting the runner, we first run the base_dirpath folder once, which
        # will build all of our mdscript files, and index all the dependency files.
        self.watcher.start()
        # Then, we simply start the watcher, which will always watch the entire base_dirpath
        # folder, and all of the dependencies files will have already been added to its watch.

    def start(self):
        self._start(run_tests=False)

    def start_with_tests(self):
        self._start(run_tests=True)

