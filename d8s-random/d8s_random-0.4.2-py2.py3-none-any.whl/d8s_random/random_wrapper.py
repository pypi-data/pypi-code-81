import random

from .random_wrapper_temp_utils import copy_first_arg


def random_number():
    """Return a random number in range [0.0, 1.0)."""
    return random.random()


def random_integer(a=0, b=10):
    """Return a random number between a and b (inclusive)."""
    return random.randint(a, b)


def random_xkcd_integer():
    """Get a random number using the method described here: https://xkcd.com/221/."""
    return 4


def random_dilbert_integer():
    """Get a random number using the method described here: https://dilbert.com/strip/2001-10-25c."""
    return 9


@copy_first_arg
def random_shuffle(iterable):
    """Shuffle the order of the given iterable."""
    random.shuffle(iterable)
    return iterable


def random_choice(iterable):
    """Return a random item from the iterable."""
    return random.choice(iterable)


def random_choices(iterable, n: int):
    """Return a random item from the iterable."""
    return random.choices(iterable, k=n)


def random_sample(iterable, n):
    """Return n items, selected at random, from the iterable."""
    return random.sample(iterable, n)
