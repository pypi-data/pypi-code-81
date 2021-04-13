from .. import Puzzle
from .boards import boards

if __name__ == "__main__":
    for i, board in enumerate(boards):
        print(f"Board {i}: {board}")

        puzzle = Puzzle(board, ".")

        print(f"Puzzle {i}:\n{puzzle.to_formatted_string()}")

        puzzle.shuffle()

        print(f"Shuffled:\n{puzzle.to_formatted_string()}")
