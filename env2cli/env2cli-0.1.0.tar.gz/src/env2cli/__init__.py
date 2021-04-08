from typing import List, Callable
from os import getenv


class RequiredArgumentNotExistsError(Exception):
    def __init__(self, env):
        self.env = env
    def __str__(self):
        return 'Required argument is empty or does not exists'

class Argument:
    def __init__(
        self, 
        env : str, 
        arg_key : str =None, 
        func : Callable[[str, str], List[str]] = None, 
        required : bool = False
    ):
        self.env = env
        self.arg_key = arg_key
        self.func = func
        self.required = required

default_func = lambda key, val: [key, val]
positional_argument_func = lambda _, val: [val]
def flag_argument_func(key, val : str):
    """
    For flags argument
    example:
        Dockerfile:
            ENV MY_FLAG TRUE
        converted into " ... --my-flag"
    """
    if val.lower() == 'true':
        return [key]
    return []

def apply_arg(argv : List[str], argument : Argument):
    val = getenv(argument.env)
    if val:
        func = argument.func if argument.func else default_func
        argv += func(argument.arg_key, val)
    elif argument.required:
        raise RequiredArgumentNotExistsError(argument.env)


def bulk_apply(arguments : List[Argument], argv : List[str] = []):
    for arg in arguments:
        apply_arg(argv, arg)
    return argv