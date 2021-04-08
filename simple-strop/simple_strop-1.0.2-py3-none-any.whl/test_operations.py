from .operations import reverse, piglatin


def test_reverse():
    string = "12345"
    rev = "54321"
    assert reverse(string) == rev

    string = "11111"
    rev = string
    assert reverse(string) == rev


def test_piglatin():
    string = "This is my test string"
    pigged = "Isthay isway myay esttay ingstray"
    assert piglatin(string) == pigged

    # NOTE: this test identifies unsupported behavior, but shows how it will return the
    # wrong answer
    string = "This is my test string."
    pigged = "Isthay isway myay esttay ing.stray"
    assert piglatin(string) == pigged
