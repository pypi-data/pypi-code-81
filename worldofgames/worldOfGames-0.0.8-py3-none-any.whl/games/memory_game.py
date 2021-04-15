from worldOfGames.games.game_helper import *
import time,random
class MemoryGame(Game):
    def describe_game(self,n):
        return "\n\t{}. Memory Game - a sequence of numbers will appear for 1 second and you have to\
                \nguess it back ".format(n)

    def play_game(self):
        clear()
        min = 10**(self.difficulty+2)
        max = min*10-1 
        correct_answer = random.randint(min,max)
        print(correct_answer)
        time.sleep(1)
        clear()
        answer = input("what is the number : \t")
        check_answer(correct_answer,answer)
