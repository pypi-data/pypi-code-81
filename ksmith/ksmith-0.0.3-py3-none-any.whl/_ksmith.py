"""
This is the simple code for ksmith
Do not take it too seriously
Okay?
"""
import sys as _sys
import time as _time
import os as _os

__all__= ['hello', 'delay_print','clear','get_num','delay']

def delay(time):
    """
    A delay so I can quickly delay stuff
    """
    _time.sleep(time)

def hello(name):
    """This is a simple helo funtion that takes in a name
    and outputs it back to the user with a greeting."""
    string = f"Hello {name}, my name is Kent Smith"
    return string

def delay_print(string, level=4, end=''):
    """
    A input repeated back with with a delayed output
    """
    speed=0.01*level


    for char in string:
        _sys.stdout.write(char)
        _sys.stdout.flush()
        _time.sleep(speed)
    print(end)
    return 0

def get_num(prompt="Enter a number:", start=False, finish=False, integer=False, round_up=False):
    """
    Takes a number from a person and checks that the number is valid.

    Args:
        prompt[str]: the string that shows up as the prompt (*: * are added the end of the string)
        start[int or float]: the value that the number must be greater than (start < num)
        finish[int or float]: the value that the number must be less than (finish > num)
        interger[boolean]: true or false statement that decides of the value must be an int
        round_up[boolean]: true or false statement that decides if it will "round up" the number
        round_num[float]: float that will determine whether or not rounding is appropriate

    Returns:
            It returns a number that the user inputted if it meets all the args
    """
    while True:
        try:
            numb = float(input(prompt))
            if integer:
                if round_up:
                    num=numb - int(numb)
                    if num >= 0.5:
                        numb= int(numb)+1
                else:
                    numb = int(numb)
        except ValueError:
            print("Please enter a number!")
            continue
        if finish is not False:
            if start is not False:
                if numb >= start and numb <= finish:
                    return numb
                print(f"Enter a value between {start} and {finish}!")
            else:
                if numb <= finish:
                    return numb
                print(f"Enter a value below {finish}!")
                continue
        elif start is not False:
            if numb >= start:
                return numb
            print(f"Enter a value above {start}!")
            continue
        else:
            return numb


#print(get_num(start=3,finish=5,integer=True,round_up=True))    test get_num



def clear():
    """
    clears terminal
    """
    if _sys.platform.startswith('win32'):
        _os.system('cls')
    else:
        _os.system('clear')
    return 0
