import random

alphabet = {
    "a": "z", "f": "u", "k": "p", "p": "k", "u": "f", "z": "a", "4": "5", "9": "0",
    "b": "y", "g": "t", "l": "o", "q": "j", "v": "e", "0": "9", "5": "4",
    "c": "x", "h": "s", "m": "n", "r": "i", "w": "d", "1": "8", "6": "3",
    "d": "w", "i": "r", "n": "m", "s": "h", "x": "c", "2": "7", "7": "2",
    "e": "v", "j": "q", "o": "l", "t": "g", "y": "b", "3": "6", "8": "1",
}

def _binnary():
    lists = [random.randint(10, 99) for _ in range(random.randint(3, 5))]
    byte_array = bytearray(lists)
    try:
        index = random.randint(0, int(len(byte_array)))
        binnary = bin(byte_array[index])
    except IndexError:
        index = 0
        binnary = bin(byte_array[index])
    return binnary, index