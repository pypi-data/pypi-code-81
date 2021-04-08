import re
from colorama import Fore, Back

END = "\033[0m"
GREY = "\33[90m"


def strip_special_characters(some_string: str) -> str:
    """Remove all special characters, punctuation, and spaces from a string"""
    # Input: "Special $#! characters   spaces 888323"
    # Output: 'Specialcharactersspaces888323'
    result = ''.join(e for e in some_string if e.isalnum())
    return result


def print_red(string):
    print(f"{Fore.RED}{string}{END}")


def print_yellow(string):
    print(f"{Fore.YELLOW}{string}{END}")


def print_blue(string):
    print(f"{Fore.BLUE}{string}{END}")


def print_green(string):
    print(f"{Fore.GREEN}{string}{END}")


def print_grey(string):
    print(f"{GREY}{string}{END}")
    # Color code from here: https://stackoverflow.com/a/39452138


def print_warning(message: str):
    print_red(r"""

     ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄        ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄        ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄  ▄  ▄ 
    ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░▌      ▐░▌▐░░░░░░░░░░░▌▐░░▌      ▐░▌▐░░░░░░░░░░░▌▐░▌▐░▌▐░▌
    ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌░▌     ▐░▌ ▀▀▀▀█░█▀▀▀▀ ▐░▌░▌     ▐░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌▐░▌▐░▌
    ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌▐░▌    ▐░▌     ▐░▌     ▐░▌▐░▌    ▐░▌▐░▌          ▐░▌▐░▌▐░▌
    ▐░▌   ▄   ▐░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌ ▐░▌   ▐░▌     ▐░▌     ▐░▌ ▐░▌   ▐░▌▐░▌ ▄▄▄▄▄▄▄▄ ▐░▌▐░▌▐░▌
    ▐░▌  ▐░▌  ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌  ▐░▌  ▐░▌     ▐░▌     ▐░▌  ▐░▌  ▐░▌▐░▌▐░░░░░░░░▌▐░▌▐░▌▐░▌
    ▐░▌ ▐░▌░▌ ▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀█░█▀▀ ▐░▌   ▐░▌ ▐░▌     ▐░▌     ▐░▌   ▐░▌ ▐░▌▐░▌ ▀▀▀▀▀▀█░▌▐░▌▐░▌▐░▌
    ▐░▌▐░▌ ▐░▌▐░▌▐░▌       ▐░▌▐░▌     ▐░▌  ▐░▌    ▐░▌▐░▌     ▐░▌     ▐░▌    ▐░▌▐░▌▐░▌       ▐░▌ ▀  ▀  ▀ 
    ▐░▌░▌   ▐░▐░▌▐░▌       ▐░▌▐░▌      ▐░▌ ▐░▌     ▐░▐░▌ ▄▄▄▄█░█▄▄▄▄ ▐░▌     ▐░▐░▌▐░█▄▄▄▄▄▄▄█░▌ ▄  ▄  ▄ 
    ▐░░▌     ▐░░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌      ▐░░▌▐░░░░░░░░░░░▌▐░▌      ▐░░▌▐░░░░░░░░░░░▌▐░▌▐░▌▐░▌
     ▀▀       ▀▀  ▀         ▀  ▀         ▀  ▀        ▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀        ▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀  ▀  ▀ 
    """)
    print("\n")
    print_red("WARNING:")
    confirm = input(f"{message}. Are you sure you want to do that? [y/N]")
    if confirm.lower() == 'y':
        return True
    else:
        return False


def chomp(string):
    """This chomp cleans up all white-space, not just at the ends"""
    string = str(string)
    result = string.replace("\n", " ")  # Convert line ends to spaces
    result = re.sub(" [ ]*", " ", result)  # Truncate multiple spaces to single space
    result = result.replace(" ", "")
    result = result.replace(u"\xa0", u" ")  # Remove non-breaking space
    result = re.sub("^[ ]*", "", result)  # Clean start
    return re.sub("[ ]*$", "", result)  # Clean end


def chomp_keep_single_spaces(string):
    """This chomp cleans up all white-space, not just at the ends"""
    string = str(string)
    result = string.replace("\n", " ")  # Convert line ends to spaces
    result = re.sub(" [ ]*", " ", result)  # Truncate multiple spaces to single space
    result = result.replace(" ", " ")  # Replace weird spaces with regular spaces
    result = result.replace(u"\xa0", u" ")  # Remove non-breaking space
    result = re.sub("^[ ]*", "", result)  # Clean start
    return re.sub("[ ]*$", "", result)  # Clean end
