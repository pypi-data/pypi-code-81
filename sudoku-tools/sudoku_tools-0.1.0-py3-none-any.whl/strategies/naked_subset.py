from __future__ import annotations

from typing import TYPE_CHECKING

from .strategy import Strategy

if TYPE_CHECKING:
    from ..puzzle import Puzzle, T


class NakedSubset(Strategy):
    """
    Apply the [Naked Subset](http://sudopedia.enjoysudoku.com/Naked_Subset.html) strategy
    """

    __slots__ = ("size",)

    def __init__(self, size: int):
        super().__init__(difficulty=0.323 * size)
        self.name += f" - {size}"
        self.size = size

    def __call__(self, puzzle: Puzzle[T]) -> int:
        if self.size <= 0 or self.size >= puzzle.order:
            return 0

        complement_size = puzzle.order - self.size
        if complement_size < self.size:
            from .hidden_subset import HiddenSubset

            return HiddenSubset(complement_size)(puzzle)

        candidate_eliminations = 0
        for b, blank in puzzle._blank():
            if len(blank.candidates) == self.size:
                for house in [puzzle._row, puzzle._col, puzzle._box]:
                    complement = set(
                        p
                        for p, peer in house(b)
                        if (
                            len(peer.candidates) > self.size
                            or any((pc not in blank.candidates) for pc in peer.candidates)
                        )
                    )
                    if len(complement) == complement_size:
                        for p in complement:
                            for c in blank.candidates:
                                if c in puzzle.cells[p].candidates:
                                    puzzle.cells[p].candidates.remove(c)
                                    candidate_eliminations += 1

        return candidate_eliminations


class NakedSingle(NakedSubset):
    """
    The [Naked Single](http://sudopedia.enjoysudoku.com/Naked_Single.html) strategy
    """

    def __init__(self):
        super().__init__(1)


class ForcedDigit(NakedSingle):
    """
    Alias for the [[NakedSingle]] strategy
    """


class SoleCandidate(NakedSingle):
    """
    Alias for the [[NakedSingle]] strategy
    """


class NakedDouble(NakedSubset):
    """
    Apply the [Naked Double](http://sudopedia.enjoysudoku.com/Naked_Double.html) strategy
    """

    def __init__(self):
        super().__init__(2)


class NakedTriple(NakedSubset):
    """
    Apply the [Naked Triple](http://sudopedia.enjoysudoku.com/Naked_Triple.html) strategy
    """

    def __init__(self):
        super().__init__(3)


class NakedQuad(NakedSubset):
    """
    Apply the [Naked Quad](http://sudopedia.enjoysudoku.com/Naked_Quad.html) strategy
    """

    def __init__(self):
        super().__init__(4)


__all__ = ("ForcedDigit", "NakedDouble", "NakedQuad", "NakedSingle", "NakedSubset", "NakedTriple")
