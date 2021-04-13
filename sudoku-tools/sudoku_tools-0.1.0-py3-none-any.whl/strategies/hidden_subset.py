from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from .strategy import Strategy

if TYPE_CHECKING:
    from ..puzzle import Puzzle, T


class HiddenSubset(Strategy):
    """
    Apply the [Hidden Subset](http://sudopedia.enjoysudoku.com/Hidden_Subset.html) strategy
    """

    __slots__ = ("size",)

    size: int

    def __init__(self, size):
        super().__init__(difficulty=0.163 * size)
        self.name += f" - {size}"
        self.size = size

    def __call__(self, puzzle: Puzzle[T]) -> int:
        if self.size <= 0 or self.size >= puzzle.order:
            return 0

        complement_size = puzzle.order - self.size
        if complement_size < self.size:
            from .naked_subset import NakedSubset

            return NakedSubset(complement_size)(puzzle)

        candidate_eliminations = 0
        for b, blank in puzzle._blank():
            if len(blank.candidates) >= self.size:
                for house in [puzzle._row, puzzle._col, puzzle._box]:
                    for hidden_candidates in itertools.combinations(blank.candidates, self.size):
                        subset = set(
                            p for p, peer in house(b) if (any((hc in peer.candidates) for hc in hidden_candidates))
                        )
                        subset.add(b)

                        if len(subset) == self.size:
                            for s in subset:
                                before_size = len(puzzle.cells[s].candidates)
                                puzzle.cells[s].candidates = set(hidden_candidates)
                                after_size = len(puzzle.cells[s].candidates)
                                candidate_eliminations += before_size - after_size

        return candidate_eliminations


class HiddenSingle(HiddenSubset):
    """
    The [Hidden Single](http://sudopedia.enjoysudoku.com/Hidden_Single.html) strategy
    """

    def __init__(self):
        super().__init__(1)


class PinnedDigit(HiddenSingle):
    """
    Alias for the [[HiddenSingle]] strategy
    """


__all__ = ("HiddenSubset", "HiddenSingle", "PinnedDigit")
