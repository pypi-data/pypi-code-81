from d8s_regexes import is_regex, regex_closest_match, regex_create, regex_simplify


def test_is_regex_1():
    assert is_regex('foo bar')
    assert not is_regex('(')


def test_regex_closest_match_1():
    regex = 'foo[a-z]'
    s = 'foo bar'
    result = regex_closest_match(regex, s)
    assert result == 'foo'

    regex = 'when in the  course'
    s = 'when in the course'
    result = regex_closest_match(regex, s)
    assert result == 'when in the '

    regex = 'ab'
    s = 'z'
    result = regex_closest_match(regex, s)
    assert result == ''

    regex = '[ab]'
    s = 'z'
    result = regex_closest_match(regex, s)
    assert result == ''


def test_regex_create_1():
    l = ['aba', 'abb', 'acd']
    assert regex_create(l) == 'a[bc][abd]'

    l = ['af', 'abcf', 'abcdef']
    assert regex_create(l) == 'a[bf]c?[df]?e?f?'

    l = ['111111', '999999']
    assert regex_create(l) == '[19]{6}'

    l = ['111111', '999999']
    assert regex_create(l, simplify_regex=False) == '[19][19][19][19][19][19]'

    l = ['abc', 'ebd', 'cbc']
    assert regex_create(l) == '[ace]b[cd]'
    assert regex_create(l, simplify_regex=False) == '[ace]b[cd]'


def test_regex_simplify_1():
    s = '[19]'
    assert regex_simplify(s) == '[19]'

    s = '[19][19]'
    assert regex_simplify(s) == '[19]{2}'

    s = '[19][19][19]'
    assert regex_simplify(s) == '[19]{3}'

    s = '[19][19][19][19][19]'
    assert regex_simplify(s) == '[19]{5}'

    s = '[19][19][19][19][19][19][19][19][19][19]'
    assert regex_simplify(s) == '[19]{10}'

    s = '[Az]'
    assert regex_simplify(s) == '[Az]'

    s = '[Az][Az]'
    assert regex_simplify(s) == '[Az]{2}'

    s = '[Az][Az][Az]'
    assert regex_simplify(s) == '[Az]{3}'

    s = '[Az][Az][Az][Az][Az]'
    assert regex_simplify(s) == '[Az]{5}'

    s = '[Az][Az][Az][Az][Az][Az][Az][Az][Az][Az]'
    assert regex_simplify(s) == '[Az]{10}'

    s = 'https://pastebin.com/raw/[23DLSXZamv][1FNSYcfqr][59BEGHRWcj][4HLVnpqru][49EKNPgnqz][56ABEJLUns][48BUZfpuw][14CDSVWjs]'
    assert regex_simplify(s) == 'https://pastebin.com/raw/[a-zA-Z0-9]{8}'

    s = 'https://pastebin.com/raw/[23DLSXZamv][1FNSYcfqr][59BEGHRWcj][4HLVnpqru][49EKNPgnqz][56ABEJLUns][48BUZfpuw][14CDSVWjs]'
    assert (
        regex_simplify(s, consolidation_threshold=20)
        == 'https://pastebin.com/raw/[23DLSXZamv][1FNSYcfqr][59BEGHRWcj][4HLVnpqru][49EKNPgnqz][56ABEJLUns][48BUZfpuw][14CDSVWjs]'
    )

    s = '[ab]c[ab]'
    assert regex_simplify(s) == '[ab]c[ab]'
