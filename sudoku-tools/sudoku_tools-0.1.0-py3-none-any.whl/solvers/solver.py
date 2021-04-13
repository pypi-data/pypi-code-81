from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..puzzle import Puzzle, T


class Solver(ABC):
    @abstractmethod
    def solve(self, puzzle: Puzzle[T]) -> bool:
        """Solve the puzzle in place.

        Args:
            puzzle (Puzzle): The puzzle to be solved.

        Returns:
            bool: Whether or not the puzzle is solved.
        """
        ...


__all__ = ("Solver",)
