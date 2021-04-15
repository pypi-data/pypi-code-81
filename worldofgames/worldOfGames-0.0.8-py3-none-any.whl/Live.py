import os,time 
from worldOfGames.games.game_helper import *

#getting all the game modules from the game directory
game_files = os.listdir("worldOfGames/games")
games = []
#loading the game modules and saving a class instence for each game in the 'games' array 
for game_file in game_files:
    if (game_file[-3:] == '.py' and game_file[:-3] not in ["game_helper",'__init__']):
        file_name = 'worldOfGames.games.'+game_file[:-3]
        class_name = game_file[:-3].title().replace("_","")
        module = (__import__(file_name, globals(), locals(), [class_name[:-3]]))
        game_class = eval("module"+"."+class_name + "()")
        games.append(game_class)
    
def welcome(name):
    clear()
    return "\nHello {} and welcome to the World of Games (WoG). \
          \nHere you can find many cool games to play.\n\n".format(name)

def load_game():
    game_num = 0
    game_chosen = False
    while (game_num not in [*range(1,len(games)+1)]):
        if (game_chosen):
            print("\n\nYour answer should be between 1 and {}.\
                \n\nHere are the options again:\n\n".format(len(games)))
        woginfo = "Please choose a game to play:"
        for i in range(len(games)):
            woginfo+=games[i].describe_game(i+1)
        game_num = input(woginfo + "\n\n")
        game_chosen = True
        if game_num.isdigit():
            game_num = int(game_num)
    difficulty = choose_difficulty()
    return game_num,difficulty

#getting the difficulty from the user and validating the value
def choose_difficulty():
    difficulty = ""
    difficulty_chosen = False
    while (difficulty not in [*range(1,6)]):
        clear()
        if (difficulty_chosen):
            print("Your answer sholud be a number between 1 to 5\n")
        difficulty = input("\n\nPlease choose game difficulty from 1 to 5:\t")
        difficulty_chosen = True
        print("\n\n")
        if difficulty.isdigit():
            difficulty = int(difficulty)
    return difficulty

def start_game(game_num,difficulty):
    want_to_play = "yes"
    played = False
    while want_to_play in ["yes","yahh","y","sure"]:
        game = games[game_num - 1]
        game.set_difficulty(difficulty)
        if played:
            change_or_not = input("Would you like to play the same difficulty? ")
            if change_or_not not in ["yes","yahh","y","sure"]:
                new_difficulty = choose_difficulty()
                game.set_difficulty(new_difficulty)
        game.play_game()
        played=True
        want_to_play = input("\n\ndo you want to play the same game again?\n")
        clear()
        

def play(name):
    print(welcome(name))
    want_to_play = "yes"
    while want_to_play in ["yes","yahh","y","sure"]:
        game_num,difficulty = load_game()
        start_game(game_num,difficulty)
        want_to_play = input("\n\nWould you like to play a diffrent game?\n")
        clear()
    if want_to_play not in ["yes","yahh","y","sure"]:
        clear()
        print("\n\nGoodbye, It was fun playing with you\n\n")


