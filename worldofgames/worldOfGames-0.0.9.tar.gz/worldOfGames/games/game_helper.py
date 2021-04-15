
from os import system, name 

#the game abstract class
class Game():
    def __init__(self):
        self.difficulty = 1
        self.description = ""
    def describe_game(self,n):
        pass
    def play_game(self):
        pass
    def set_difficulty(self,num):
        self.difficulty = num 

#clear the terminal
def clear(): 
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear')

#checks if the answer is valid, inform the user and ask if to start a new game
def check_answer(correct_answer,answer):
    if answer.isdigit():
        answer = int(answer)
    if answer == correct_answer:
        print('\033[92m'+'Correct'+'\033[0m')
    else :
        print('\033[31m'+"wrong!")
        print('\033[0m'+f"Correct answer: {correct_answer}\nYour answer: {answer}")

#asks the user if they want to keep playing and say goodabye otherwise
def check_will():
    still_wanna_play = input("\n\nNew game?    \n\n")
    clear()
    if (still_wanna_play not in ["yes","y","sure","ok","Y","Yes"]):
        print("\n\nIt was fun playing, goodbye \n\n")