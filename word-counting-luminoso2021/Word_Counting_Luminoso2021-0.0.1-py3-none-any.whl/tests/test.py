import pytest
from word_count import word_count

# Checking JSON format for file 1
def test1():
    assert word_count("test1.txt", "JSON") == '{"i": 2, "swim": 2, "to": 2, "go": 1, "love": 1, "will": 1}'

# Checking JSON format for file 2
def test2():
    assert word_count("test2.txt", "JSON") == '{"dream": 2, "a": 1, "get": 1, "have": 1, "i": 1, "is": 1, "lamborgini": 1, "my": 1, "to": 1}'

# Checking 10th item for human readable format for file 3
def test3():
    assert word_count("test3.txt") == 'am - 2'

# Checking 10th item for human readable format for file 4
def test4():
    assert word_count("test4.txt") == 'his - 86'