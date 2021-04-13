from .. import Puzzle
from .boards import boards

if __name__ == "__main__":
    for i, board in enumerate(boards):
        print(f"Board {i}: {board}")

        puzzle = Puzzle(board, ".")

        print(f"Puzzle {i}:\n{puzzle.to_formatted_string()}")

        candidate_eliminations = puzzle.solve()

        print(f"Solution:\n{puzzle.to_formatted_string()}")

        print(candidate_eliminations)
