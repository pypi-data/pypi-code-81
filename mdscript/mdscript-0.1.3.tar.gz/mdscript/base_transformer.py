from mdscript.runner import Runner
from abc import abstractmethod
from typing import Optional


class BaseTransformer:
    def __init__(self, runner: Runner, source_filepath: str, attribute: Optional[str]):
        self.runner = runner
        self.source_filepath = source_filepath
        self.attribute = attribute

    @abstractmethod
    def transform(self) -> str:
        raise Exception(f"transform function must be implemented")

    def test(self) -> bool:
        # The implementation of the test function is optional, hence the missing @abstractmethod.
        # If the test function is not implemented, we return True so that it will be considered as passed.
        return True
