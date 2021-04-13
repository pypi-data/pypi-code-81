from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from ..strategies import HiddenSubset, NakedSubset, RefreshCandidates, Strategy
from .solver import Solver

if TYPE_CHECKING:
    from ..puzzle import Puzzle, T


def essential_strategies(order: int) -> Generator[Strategy, None, None]:
    """
    Generator for strategies from simple to complex with a given order
    """
    yield RefreshCandidates()
    for s in range(1, order // 2):
        yield NakedSubset(s)
        yield HiddenSubset(s)


class StrategySolver(Solver):
    def solve(self, puzzle: Puzzle[T]) -> bool:
        """
        Solve the puzzle using strategies

        Returns:
            bool: A boolean value indicating whether the puzzle could be solved
        """
        if puzzle.has_conflicts():
            return False

        while not puzzle.is_solved():
            changed = False

            for strategy in essential_strategies(puzzle.order):
                if strategy(puzzle) > 0:
                    changed = True
                    break
            if not changed:
                return False

        return True


__all__ = ("StrategySolver", "essential_strategies")
