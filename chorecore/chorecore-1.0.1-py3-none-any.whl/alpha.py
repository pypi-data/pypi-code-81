import string


class Alphabet:
	class Strings:
		LOWERCASE = string.ascii_lowercase
		UPPERCASE = string.ascii_uppercase
		LOWERCASE_VOWELS = "aeiouy"
		UPPERCASE_VOWELS = "AEIOUY"
		LOWERCASE_NON_VOWELS = "bcdfghjklmnpqrstvwxz"
		UPPERCASE_NON_VOWELS = "BCDFGHJKLMNPQRSTVWXZ"

	LOWERCASE = list(Strings.LOWERCASE)
	UPPERCASE = list(Strings.UPPERCASE)
	LOWERCASE_VOWELS = list(Strings.LOWERCASE_VOWELS)
	UPPERCASE_VOWELS = list(Strings.UPPERCASE_VOWELS)
	LOWERCASE_NON_VOWELS = list(Strings.LOWERCASE_NON_VOWELS)
	UPPERCASE_NON_VOWELS = list(Strings.UPPERCASE_NON_VOWELS)


def lowercase_at(i):
	return Alphabet.LOWERCASE[i % 26]


def uppercase_at(i):
	return Alphabet.UPPERCASE[i % 26]


def lowercase_vowel_at(i):
	return Alphabet.LOWERCASE_VOWELS[i % 26]


def uppercase_vowel_at(i):
	return Alphabet.UPPERCASE_VOWELS[i % 26]


def lowercase_non_vowel_at(i):
	return Alphabet.LOWERCASE_NON_VOWELS[i % 26]


def uppercase_non_vowel_at(i):
	return Alphabet.UPPERCASE_NON_VOWELS[i % 26]
