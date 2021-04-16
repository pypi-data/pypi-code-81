import typing

from ahocorapy.keywordtree import KeywordTree


class Encode:
    def __init__(self, name: str, advice: str, patterns: tuple):
        self.name = name
        self.advice = advice
        self.keyword_tree = self._build_keyword_tree(patterns)

    @staticmethod
    def _build_keyword_tree(patterns: tuple) -> KeywordTree:
        keyword_tree = KeywordTree()
        for pattern in patterns:
            keyword_tree.add(pattern)
        keyword_tree.finalize()
        return keyword_tree

    def check(self, text: str) -> bool:
        if not text:
            return False
        if not isinstance(text, str):
            text = str(text)
        match = self.keyword_tree.search(text)
        return match is not None

    def find_all(self, text: str) -> typing.Iterable[typing.Tuple[str, int]]:
        if not text:
            return tuple()
        return self.keyword_tree.search_all(text)
