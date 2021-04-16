from .clearscreen import *
from .pressanykey import *
from .standtextout import *
from .multiprint import *
from .sanitiseinput import *
"""
FUNCTIONS
    clearScreen()
        Credit:
        https://www.sololearn.com/Discuss/764024/how-to-clear-the-screen-in-python-terminal

    clearScreenOld()
        This will NOT work on windows unless you have colorama package. Tries three times to clear the screen.

    clearScreenV1()
        Harder to understand but not many lines (can be shortened to two by putting imports on the same line, and removing the del statement). Doesn't work if the user doesn't have `clear' or `cls' installed.

    standTextOut(string, printMechanismDash=<built-in function print>, printMechanismString=<built-in function print>)
        param string: the string to sandwich in between the dashes.
        param printMechanismDash: how it will output the dashes. e.g. do `logging.info' to output it with logging.info. Defaults to print.
            ***IF YOU CHOOSE A PRINT MECHANISM IT NEEDS TO BE IMPORTED IN YOUR ORIGINAL PROGRAM, **NOT** THIS MODULE! How does it work?! you pass the function of output and it uses it.
        param printMechanismString: how it will output the string that is sandwidched in between the dashes. Defaults to print.
            ***READ THE ABOVE IMPORTANT NOTICE (of printMechanismDash)!!!***

    standTextOut_Return(string)
        Will return the finished string so you can output it the way you want.
pressanykey(string='Press any key to continue...', verbose=True)
        SOURCE: https://raw.githubusercontent.com/TheTechRobo/python-text-calculator/master/FOR%20CLEARING%20THE%20SCREEN%20AND%20PRESS%20ANY%20KEY%20TO%20CONTINUE.md
    multiprint(stuffToPrint, _=None, **kwargs)
        Accepts a dictionary. With key/value pairs text/function.
        For example, you might pass {"Welcome to ": cprint.info, "Palc": cprint.ok, "!" + MANYSPACE: cprint.info}
        which will run cprint.info("Welcome to ");cprint.ok("Palc");cprint.info("!" + MANYSPACE)
        Setting gettext to True will run whateverFunctionYouPassed(_(item), *args, **kwargs) instead of just whateverFunctionYouPassed(item, *args, **kwargs). 
        The **kwargs is given to EVERY function. Useful as an "end=True" or similar.

    CleanInput(inp, customRules=[], appendList=True)
        Still not perfect, but gets rid of the common culprits (\, ', and zero-width space), and strip()s the text.
        Then, you can add a list as the second argument (optional) which allows you to add more stuff.
        Set appendList to False if you ONLY want to use the custom rules.
        For example, you might run:
        turbofunc.CleanInput("   This input is NOT CLEAN!sss\", ["sss","!"], appendList=True)
        That will turn the string passed in from "   This input is NOT CLEAN!sss\" to "This input is NOT CLEAN".
        Note that the custom rules are done before the defaults.
"""
