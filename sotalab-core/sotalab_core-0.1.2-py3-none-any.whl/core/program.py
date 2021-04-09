from typing import List

from .config.registry import register


@register
class Program:
    def run(self, args: List[str]):
        raise NotImplementedError
