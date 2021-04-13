from __future__ import annotations

import random
from collections import defaultdict
from copy import deepcopy
from typing import Any, DefaultDict, Generic, List, Sequence, Set, Type, TypeVar

import numpy as np

from .solvers import Solver
from .solvers.strategy_solver import StrategySolver, essential_strategies

T = TypeVar("T", bound=Any)


class Puzzle(Generic[T]):
    """
    The base class for a sudoku puzzle.
    ```

    Args:
        Generic (T): The base type for each token in the sudoku puzzle

    Attributes:
        tokens (Tokens): A list of the tokens in use in the sudoku puzzle as identified by their integer aliases,
            which are the respective indices of this list.
        order (int): The number of unique tokens in use in the puzzle. For the common 9x9 sudoku puzzle,
            this value is 9.
        cells (List[Cell]): A list of all the cells in the sudoku puzzle.
    """

    __slots__ = "order", "tokens", "cells"

    order: int
    tokens: Tokens
    cells: List[Cell]

    class Tokens(List[T]):
        """
        A list of the tokens in use in the sudoku puzzle as identified by their integer aliases,
        which are the respective indices of this list.
        """

        def swap(self, i: int, j: int):
            """
            Switch the positions of two sets of tokens in the puzzle by switching their respective aliases.

            Args:
                i (int): The integer alias value associated with a token
                j (int): The integer alias value associated with a token
            """
            self[i], self[j] = self[j], self[i]

        def shuffle(self):
            """
            Randomly swap the tokens in the puzzle by randomizing their integer aliases.
            """
            tokens = self[1:]
            random.shuffle(tokens)
            self[1:] = tokens

    class Cell:
        """
        The class for an individual cell in the sudoku puzzle

        Attributes:
            puzzle (Puzzle): The corresponding sudoku puzzle
            candidates (Set[int]): A set of the cell's remaining candidates
            value (int): The value of the sudoku cell or 0 if it is blank.
        """

        __slots__ = "puzzle", "candidates"

        puzzle: Puzzle
        candidates: Set[int]

        def __init__(self, puzzle: Puzzle[T], value: int):
            self.puzzle = puzzle
            self.candidates = {i + 1 for i in range(self.puzzle.order)}
            self.value = value

        @property
        def value(self) -> int:
            if len(self.candidates) > 1:
                return 0
            return next(iter(self.candidates))

        @value.setter
        def value(self, value: int):
            if value == 0:
                self.candidates = {i + 1 for i in range(self.puzzle.order)}
            else:
                self.candidates = {value}

        def is_blank(self) -> bool:
            """
            Check whether the cell is blank or has a value.

            Returns:
                bool: A boolean value for whether the cell is blank.
            """
            return len(self.candidates) > 1

    def _box(self, index: int):
        boxWidth = int(self.order ** 0.5)
        row = index // self.order
        col = index % self.order
        edgeRow = boxWidth * (row // boxWidth)
        edgeCol = boxWidth * (col // boxWidth)

        for i in range(self.order):
            r = edgeRow + i // boxWidth
            c = edgeCol + (i % boxWidth)
            if not (r == row and c == col):
                p = int(self.order * r + c)
                yield p, self.cells[p]

    def _row(self, index: int):
        row = index // self.order
        col = index % self.order

        for i in range(self.order):
            if i != col:
                p = int(self.order * row + i)
                yield p, self.cells[p]

    def _col(self, index: int):
        row = index // self.order
        col = index % self.order

        for i in range(self.order):
            if i != row:
                p = int(self.order * i + col)
                yield p, self.cells[p]

    def _peers(self, index: int):
        boxWidth = int(self.order ** 0.5)
        row = index // self.order
        col = index % self.order
        edgeM = boxWidth * (row // boxWidth)
        edgeN = boxWidth * (col // boxWidth)

        peers = set()

        for i in range(self.order):
            r = edgeM + i // boxWidth
            c = edgeN + i % boxWidth
            if i != col:
                p = int(self.order * row + i)
                if p not in peers:
                    yield p, self.cells[p]
                    peers.add(p)
            if i != row:
                p = int(self.order * i + col)
                if p not in peers:
                    yield p, self.cells[p]
                    peers.add(p)
            if not (r == row and c == col):
                p = int(self.order * r + c)
                if p not in peers:
                    yield p, self.cells[p]
                    peers.add(p)

    def _blank(self, indices=None):
        if indices is None:
            indices = range(self.order ** 2)
        for i in indices:
            cell = self.cells[i]
            if cell.is_blank():
                yield i, cell

    def has_conflicts(self) -> bool:
        """
        A method to determine if the board has any conflicting cells

        Returns:
            bool: True if the board has conflicts, False otherwise
        """
        for i, cell in enumerate(self.cells):
            if not cell.is_blank():
                for _, peer in self._peers(i):
                    if not peer.is_blank() and cell.value == peer.value:
                        return True
        return False

    def __init__(self, puzzle: Sequence[T], blank: T):
        """
        The object can be constructed with any 1-dimensional iterable:
        ```python
        arr_1d = [1, 0, 3, 4, 0, 4, 1, 0, 0, 3, 0, 1, 4, 0, 2, 3]
        puzzle = Puzzle(arr_1d, 0)
        ```

        Args:
            puzzle (Sequence[T]): A sequence representing a Sudoku puzzle
            blank (T): The value used to represent a blank cell
        """
        self.order = int(len(puzzle) ** 0.5)
        self.tokens = self.Tokens([blank])
        self.cells = np.empty(len(puzzle), dtype=object).tolist()

        for i, token in enumerate(puzzle):
            try:
                v = self.tokens.index(token)
            except ValueError:
                self.tokens.append(token)
                v = len(self.tokens) - 1
            self.cells[i] = self.Cell(self, v)

    def _shift_indices(self, *indices: int) -> None:
        tmp = self.cells[indices[0]]
        for i in range(1, len(indices)):
            self.cells[indices[i - 1]] = self.cells[indices[i]]
        self.cells[indices[-1]] = tmp

    def reflect(self, direction: str = "horizontal") -> None:
        """
        Reflect the Sudoku board horizontally or vertically

        Args:
            direction (str): The direction over which to reflect. Defaults to "horizontal".
        """
        n = self.order
        x = n // 2
        y = n - 1
        if direction == "horizontal":
            for i in range(n):
                for j in range(x):
                    self._shift_indices(n * i + j, n * i + (y - j))
        else:
            for i in range(x):
                for j in range(n):
                    self._shift_indices(n * i + j, n * (y - i) + j)

    def rotate(self, rotations=1) -> None:
        """
        Rotate the Sudoku board clockwise a given number in times.

        Args:
            rotations (int): The number in clockwise rotations to be performed.
                This value may be negative and is rounded to the nearest integer.
                Defaults to 1.
        """
        if not isinstance(rotations, int):
            rotations = round(rotations)
        if rotations % 4 == 0:
            return
        elif rotations % 2 == 0:
            self.cells = np.flip(self.cells)
            return
        elif rotations < 0:
            self.rotate(-1 * rotations + 2)
        else:
            n = self.order
            x = n // 2
            y = n - 1
            for i in range(x):
                for j in range(i, y - i):
                    self._shift_indices(n * i + j, n * (y - j) + i, n * (y - i) + y - j, n * j + y - i)

            self.rotate(rotations - 1)

    def transpose(self) -> None:
        """
        Switch the rows and columns in the Sudoku board
        """
        n = self.order
        for i in range(n):
            for j in range(i + 1, n):
                self._shift_indices(n * i + j, n * j + i)

    def shuffle(self) -> None:
        """
        Shuffle the board using rotations, reflections, and token-swapping
        """
        self.tokens.shuffle()
        for _ in range(self.order // 2):
            self.reflect(random.choice(("horizontal", "vertical")))
            self.rotate(random.choice(range(4)))

    def to_1D(self) -> List[T]:
        """
        A method for getting back the Sudoku board as a 1-dimensional array

        Returns:
            List[T]: A 1D array of the Sudoku board in the board's original type
        """
        return [self.tokens[c.value] for c in self.cells]

    def to_2D(self) -> List[List[T]]:
        """
        A method for getting back the Sudoku board as a 2-dimensional array

        Returns:
            List[T]: A 2D array of the Sudoku board in the board's original type
        """
        return np.reshape(self.to_1D(), (self.order, self.order)).tolist()

    def to_string(self) -> str:
        """
        A method for getting back the Sudoku board as a string

        Returns:
            str: A string representation in the Sudoku board
        """
        return "".join((str(c) for c in self.to_1D()))

    def to_formatted_string(
        self,
        cell_corner="┼",
        box_corner="╬",
        top_left_corner="╔",
        top_right_corner="╗",
        bottom_left_corner="╚",
        bottom_right_corner="╝",
        inner_top_tower_corner="╦",
        inner_bottom_tower_corner="╩",
        inner_left_floor_corner="╠",
        inner_right_floor_corner="╣",
        cell_horizontal_border="─",
        box_horizontal_border="═",
        cell_vertical_border="│",
        box_vertical_border="║",
        blank=" ",
    ) -> str:
        """
        A method for getting back the Sudoku board as a formatted string

        Returns:
            str: A formatted string representing the Sudoku board
        """
        unit = int(self.order ** 0.5)
        token_width = max([len(str(t)) for t in self.tokens])

        cell_width = token_width + 2
        box_width = unit * (cell_width + 1) - 1

        top_border = (
            top_left_corner
            + box_horizontal_border * (box_width)
            + (inner_top_tower_corner + box_horizontal_border * (box_width)) * (unit - 1)
            + top_right_corner
        )
        bottom_border = (
            bottom_left_corner
            + box_horizontal_border * (box_width)
            + (inner_bottom_tower_corner + box_horizontal_border * (box_width)) * (unit - 1)
            + bottom_right_corner
        )
        floor_border = (
            inner_left_floor_corner
            + box_horizontal_border * (box_width)
            + (box_corner + box_horizontal_border * (box_width)) * (unit - 1)
            + inner_right_floor_corner
        )
        bar_border = (
            box_vertical_border
            + cell_horizontal_border * (cell_width)
            + (cell_corner + cell_horizontal_border * (cell_width)) * (unit - 1)
        ) * (unit) + box_vertical_border

        formatted_str = f"{top_border}\n{box_vertical_border} "
        for i, c in enumerate(self.cells):
            v = c.value
            formatted_str += f"{self.tokens[v] if not c.is_blank() else blank} "
            if (i + 1) % (self.order * unit) == 0:
                if i + 1 == len(self.cells):
                    formatted_str += f"{box_vertical_border}\n{bottom_border}"
                else:
                    formatted_str += f"{box_vertical_border}\n{floor_border}\n{box_vertical_border} "
            elif (i + 1) % self.order == 0:
                formatted_str += f"{box_vertical_border}\n{bar_border}\n{box_vertical_border} "
            elif (i + 1) % unit == 0:
                formatted_str += f"{box_vertical_border} "
            else:
                formatted_str += f"{cell_vertical_border} "

        return formatted_str

    def is_solved(self) -> bool:
        """
        Check whether the puzzle is solved

        Returns:
            bool: A boolean value indicating whether the puzzle is solved
        """
        return not any(c.is_blank() for c in self.cells) and not self.has_conflicts()

    def solve(self, solver: Type[Solver] = StrategySolver) -> bool:
        """
        Solve the puzzle using one of the solvers

        Args:
            solver (Solver, optional): The solver used to solve the puzzle. Defaults to StrategySolver.

        Returns:
            bool: A boolean value indicating whether the puzzle could be solved
        """
        return solver().solve(self)

    def has_solution(self) -> bool:
        """
        Check whether the puzzle is able to be solved

        Returns:
            bool: A boolean value indicating whether the puzzle has a solution
        """
        return deepcopy(self).solve()

    def rate(self) -> float:
        """
        Calculate the difficulty of solving the puzzle

        Returns:
            float: A difficulty rating between 0 and 1
        """
        if self.is_solved():
            return 0.0
        if self.has_conflicts():
            return 1.0

        strategy_eliminations: DefaultDict[str, int] = defaultdict(int)

        puzzle_copy = deepcopy(self)

        while not puzzle_copy.is_solved():
            changes_made = False

            for strategy in essential_strategies(puzzle_copy.order):
                eliminations = strategy(puzzle_copy)
                strategy_eliminations[strategy.name] += eliminations

                if eliminations > 0:
                    changes_made = True
                    break
            if not changes_made:
                return 1.0

        max_eliminations = self.order ** 3 - self.order ** 2

        rating = 0.0
        for strategy in essential_strategies(self.order):
            difficulty = strategy.difficulty
            eliminations = strategy_eliminations[strategy.name]
            rating += difficulty * (eliminations / max_eliminations)

        return rating


__all__ = ("Puzzle",)
