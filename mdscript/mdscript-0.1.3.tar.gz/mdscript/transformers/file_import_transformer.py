from mdscript import Runner
from mdscript.base_transformer import BaseTransformer
from typing import Optional
import os


class FileImportTransformer(BaseTransformer):
    def __init__(self, runner: Runner, source_filepath: str, attribute: Optional[str]):
        super().__init__(runner=runner, source_filepath=source_filepath, attribute=attribute)

    def transform(self) -> str:
        if not os.path.isfile(self.attribute):
            raise Exception(f"File not found at {self.attribute}")

        self.runner.files_dependencies.add_dependency(
            parent_filepath=self.source_filepath,
            dependency_path=self.attribute
        )
        with open(self.attribute, 'r') as file:
            return file.read()
