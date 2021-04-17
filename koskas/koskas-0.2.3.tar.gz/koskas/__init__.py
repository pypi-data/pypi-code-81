import requests
import json
import math

__version__ = "0.2.3"
__author__ = 'Yair Koskas'


def speak():
    print('Hello, I\'m Yair Koskas')
    print('If you see this, you are a very special person!')
    print('Because you are the first person to ever care about that joke of a python package i made!')
    print('Have a nice day!')


def greet():
    print('Hello, i\'m koskas and this is my python package!')


def joke():
    r = requests.get('http://api.icndb.com/jokes/random')
    s = str(dict(json.loads(r.text)['value'])['joke'])
    s = s.replace('&quot;', '"')
    print(s)
    return 'There isn\'t a return value, only Chuck Norris'


def isprime(n):
    if type(n) != int:
        raise TypeError('Primes are whole numbers')
    if n <= 0:
        raise ArithmeticError('"Prime" is only defined for natural numbers')
    if n == 1:
        return False
    if n == 2:
        return True
    for i in range(2, math.ceil(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True
