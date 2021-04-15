from worldOfGames.games.game_helper import *
from forex_python.converter import CurrencyRates
import random

class CurrencyRoulette(Game):
    def describe_game(self,n):
        return "\n\t{}. Currency Roulette - try and guess a random value of dallors".format(n)

    def play_game(self):
        still_wanna_play = "yes"
        c = CurrencyRates()
        USD = c.get_rate('USD', 'ILS')
        clear()
        answer = input("Guess the value of USD\n\n")
        USD = str(USD)
        correct = True
        for i in range(self.difficulty+1):
            if (i == len(answer)):
                correct = False
                break
            if (USD[i] != answer[i]):
                correct = False
        if correct:
            if USD == answer:
                print('\033[92m'+'Exectly Correct'+'\033[0m')
            print('\033[92m'+'Correct,\nThat is close enough'+'\033[0m')
            print('\033[0m'+f"Correct answer: {USD}\nYour answer: {answer}")
        else:
            print('\033[31m'+"wrong!")
            print('\033[0m'+f"Correct answer: {USD}\nYour answer: {answer}")
            
