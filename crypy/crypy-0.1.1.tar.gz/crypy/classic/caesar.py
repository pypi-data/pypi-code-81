import string
from crypy.utils import lang

default_alphabet = [string.ascii_uppercase, string.ascii_lowercase]


def encrypt(data, key, alphabets=default_alphabet):
    cipher = ''
    for c in data:
        for alphabet in alphabets:
            if c in alphabet:
                cipher += alphabet[(alphabet.index(c)+key) % len(alphabet)]
                break
        else:
            cipher += c

    return cipher


def decrypt(data, key, alphabets=default_alphabet):
    return encrypt(data, -key, alphabets)


def bruteforce(data, max_key=len(default_alphabet[0]), alphabets=default_alphabet):
    return [decrypt(data, i, alphabets) for i in range(max_key)]


def breaker(data, max_key=len(default_alphabet[0]), alphabets=default_alphabet, language="en"):
    options = bruteforce(data, max_key, alphabets)
    scores = map(lambda x: (x[0], lang.get_mic(x[1], language)), enumerate(options))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores[0][0]
