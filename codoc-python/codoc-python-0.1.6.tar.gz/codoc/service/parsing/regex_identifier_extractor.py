#!/usr/bin/env python3
import inspect
import re
import types
from typing import List, Set, Type, Union

from .identifier_extractor import IdentifierExtractor


class SourceNotFoundError(Exception):
    def __init__(self, obj: Union[types.FunctionType, types.ModuleType, Type]):
        super().__init__(f"Could not find sourcecode of `{obj}`")


class RegexIdentifierExtractor(IdentifierExtractor):
    def __init__(
        self,
        obj: Union[types.FunctionType, types.ModuleType, Type],
        obj_name: str,
        identifiers_in_scope: Set[str],
    ):
        try:
            self._source_code = remove_definitions(
                remove_comments_and_strings(inspect.getsource(obj)), obj_name
            )
        except (OSError, TypeError) as e:
            try:
                # Try if it actually has a file,
                # if it does but no source, it is because the file is empty
                inspect.getfile(obj)
                self._source_code = ""
            except TypeError:
                raise SourceNotFoundError(obj) from e

        self._possible_identifiers = identifiers_in_scope

    def get_identifiers(self) -> Set[str]:
        return set(
            match
            for identifier in self._possible_identifiers
            for match in self.get_full_identifier_matches_in_code(identifier)
        )

    def get_full_identifier_matches_in_code(self, identifier: str) -> Set[str]:
        """
        Takes as input an identifier, it could be `inspect`, and returns
        a list of all matches that contain `inspect` - i.e `inspect.getsource` etc.
        """
        matches = self._get_all_matches_in_code(identifier)
        return set(match[1] for match in matches)

    def _get_all_matches_in_code(self, identifier: str) -> List[str]:
        pythonic_boundary = r"([^\d\w]|^|$)"
        return re.findall(
            pythonic_boundary
            + "("
            + identifier
            + r"(\.[\w\d_]+)*)"
            + pythonic_boundary,
            self._source_code,
            re.MULTILINE,
        )


# TODO test
def remove_definitions(code: str, obj_name: str) -> str:
    try:
        return re.sub(re.compile(f"^(def|class)[ ]+{obj_name}"), "", code)
    except re.error as e:
        raise Exception(f"Could not remove def from {obj_name}") from e


def remove_comments_and_strings(code: str) -> str:
    code = re.sub(re.compile("#.*?\n"), "", code)
    code = re.sub(re.compile('""".*?"""', re.DOTALL), "", code)
    code = re.sub(re.compile("'''.*?'''", re.DOTALL), "", code)
    code = re.sub(re.compile('".*?"'), "", code)
    code = re.sub(re.compile("'.*?'"), "", code)
    return code
