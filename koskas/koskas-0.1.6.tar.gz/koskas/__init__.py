import requests
import json
import math
__version__ = "0.1.6"
__author__ = 'Yair Koskas'
def greet():
    print('Hello, i\'m koskas and this is my python package!')


def joke():
    r = requests.get('http://api.icndb.com/jokes/random')
    s = r.text.encode('ascii')
    if type(s) != str:
        s = s.decode()
    s = s.replace('&quot;','"')
    print(dict(json.loads(r.text)['value'])['joke'])


def isprime(n):
    for i in range(2,math.ceil(math.sqrt(n))):
        if n%i == 0:
            return False
    return True


class Koskas:
    def __init__(self):
        pass

    def speak(self):
        print('Hello, I\'m Yair Koskas')
        print('If you see this, you are a very special person!')
        print('Because you are the first person to ever care about that joke of a python package i made!')
        print('Have a nice day!')
