from d8s_netstrings import (
    netstring_ascii_to_netstring_hex,
    netstring_ascii_to_string,
    netstring_hex_to_netstring_ascii,
    netstring_hex_to_string,
    string_to_netstring_ascii,
    string_to_netstring_hex,
)


def test_netstring_ascii_to_netstring_hex_1():
    results = netstring_ascii_to_netstring_hex('12:hello world!,')
    assert results == '31 32 3a 68 65 6c 6c 6f 20 77 6f 72 6c 64 21 2c'


def test_netstring_hex_to_netstring_ascii_1():
    results = netstring_hex_to_netstring_ascii('31 32 3a 68 65 6c 6c 6f 20 77 6f 72 6c 64 21 2c')
    assert results == '12:hello world!,'


def test_string_to_netstring_ascii_1():
    results = string_to_netstring_ascii('hello world!')
    assert results == '12:hello world!,'

    results = string_to_netstring_ascii('')
    assert results == '0:,'

    results = string_to_netstring_ascii('hello', 'world!')
    assert results == '17:5:hello,6:world!,,'

    results = string_to_netstring_ascii('hello', 'beautiful', 'world!')
    assert results == '29:5:hello,9:beautiful,6:world!,,'

    results = string_to_netstring_ascii('hello, world!')
    assert results == '13:hello, world!,'


def test_string_to_netstring_hex_1():
    results = string_to_netstring_hex('hello world!')
    assert results == '31 32 3a 68 65 6c 6c 6f 20 77 6f 72 6c 64 21 2c'

    results = string_to_netstring_hex('')
    assert results == '30 3a 2c'

    results = string_to_netstring_hex('hello', 'beautiful', 'world!')
    assert (
        results == '32 39 3a 35 3a 68 65 6c 6c 6f 2c 39 3a 62 65 61 75 74 69 66 75 6c 2c 36 3a 77 6f 72 6c 64 21 2c 2c'
    )


def test_netstring_ascii_to_string_1():
    results = netstring_ascii_to_string('12:hello world!,')
    assert results == 'hello world!'

    results = netstring_ascii_to_string('13:hello, world!,')
    assert results == 'hello, world!'


def test_netstring_hex_to_string_1():
    results = netstring_hex_to_string('31 32 3a 68 65 6c 6c 6f 20 77 6f 72 6c 64 21 2c')
    assert results == 'hello world!'

    results = netstring_hex_to_string(
        '32 39 3a 35 3a 68 65 6c 6c 6f 2c 39 3a 62 65 61 75 74 69 66 75 6c 2c 36 3a 77 6f 72 6c 64 21 2c 2c'
    )
    assert results == '5:hello,9:beautiful,6:world!,'
