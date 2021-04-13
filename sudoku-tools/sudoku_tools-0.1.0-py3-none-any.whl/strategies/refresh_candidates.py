from __future__ import annotations

from typing import TYPE_CHECKING

from .strategy import Strategy

if TYPE_CHECKING:
    from ..puzzle import Puzzle, T


class RefreshCandidates(Strategy):
    """
    Remove invalid candidates from each cell
    """

    def __init__(self):
        super().__init__(difficulty=0.769)

    def __call__(self, puzzle: Puzzle[T]) -> int:
        candidate_eliminations = 0
        for i, cell in enumerate(puzzle.cells):
            for _, peer in puzzle._peers(i):
                if cell.is_blank() and not peer.is_blank():
                    if peer.value in cell.candidates:
                        cell.candidates.remove(peer.value)
                        candidate_eliminations += 1
        return candidate_eliminations


__all__ = "RefreshCandidates"
