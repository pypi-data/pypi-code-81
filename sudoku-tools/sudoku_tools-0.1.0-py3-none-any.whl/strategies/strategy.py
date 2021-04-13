from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..puzzle import Puzzle, T


class Strategy:
    """
    Also known as a [Solving Technique](http://sudopedia.enjoysudoku.com/Solving_Technique.html)

    Attributes:
        name (str): The name of the strategy
        difficulty (float): The difficulty rating of the strategy defined with
            respect to eliminating a single candidate
    """

    __slots__ = "name", "difficulty"

    name: str
    difficulty: float

    def __init__(self, name=None, difficulty=None):
        self.name = name if name is not None else self.__class__.__name__
        self.difficulty = difficulty

    def __call__(self, puzzle: Puzzle[T]) -> int:
        """
        Apply the strategy to a given sudoku puzzle

        Args:
            puzzle (Puzzle[T]): The sudoku puzzle

        Returns:
            int: The number of candidates eliminated by the strategy with a
                single pass over the sudoku puzzle
        """


__all__ = ("Strategy",)
