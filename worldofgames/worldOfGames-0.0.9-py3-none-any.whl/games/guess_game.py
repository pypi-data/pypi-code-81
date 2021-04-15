from worldOfGames.games.game_helper import *
import random

class GuessGame(Game):
    def describe_game(self,n):
        return "\n\t{}. Guess Game - guess a number and see if you chose like the computer".format(n)
    def play_game(self):
        clear()
        max = 10**(self.difficulty)
        correct_answer = random.randint(1,max)
        answer = input(f"Guess a number between 1 to {max}\n\n\n\n\n")
        clear()
        check_answer(correct_answer,answer)
