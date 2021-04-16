class PathFormatter:

    def format(self, path: str) -> str:
        return path


class PrefixPathFormatter(PathFormatter):
    _version: str

    def __init__(self, prefix: str) -> None:
        self._prefix = prefix

    def format(self, path: str) -> str:
        return f'/{self._prefix}{path}'
