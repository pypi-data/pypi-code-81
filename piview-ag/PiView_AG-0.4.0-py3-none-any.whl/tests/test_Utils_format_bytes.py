from PiView_AG.Utils import Utils

short_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T',
                5: 'P', 6: 'E', 7: 'Y'}
long_labels = {0: ' ', 1: ' Kilo', 2: ' Mega', 3: ' Giga',
               4: ' Tera', 5: ' Peta', 6: ' Exa', 7: ' Yotta'}


def test_format_as_bytes():
    utils = Utils()
    results = utils.format_bytes(size=1023, style='short')
    expected = (1023, 'B')
    assert results == expected


def test_format_as_short_kilobytes():
    utils = Utils()
    results = utils.format_bytes(size=765.4 * 1024, style='short')
    expected = (765.4, 'KB')
    assert results == expected


def test_format_as_short_megabytes():
    utils = Utils()
    results = utils.format_bytes(size=1.5 * 1024 ** 2, style='short')
    expected = (1.5, 'MB')
    assert results == expected


def test_format_as_short_megabytes_2():
    utils = Utils()
    results = utils.format_bytes(size=9753 * 1024, style='short')
    expected = (9.5244140625, 'MB')
    assert results == expected


def test_format_as_short_gigabytes():
    utils = Utils()
    results = utils.format_bytes(size=3 * 1024 ** 3, style='short')
    expected = (3.0, 'GB')
    assert results == expected


def test_format_as_short_terabytes():
    utils = Utils()
    results = utils.format_bytes(size=723 * 1024 ** 4, style='short')
    expected = (723.0, 'TB')
    assert results == expected


def test_format_as_short_petabytes():
    utils = Utils()
    results = utils.format_bytes(size=1024 ** 5, style='short')
    expected = (1.0, 'PB')
    assert results == expected


def test_format_as_short_exabytes():
    utils = Utils()
    results = utils.format_bytes(size=1024 ** 6, style='short')
    expected = (1.0, 'EB')
    assert results == expected


def test_format_as_short_yottabytes():
    utils = Utils()
    results = utils.format_bytes(size=1024 ** 7, style='short')
    expected = (1.0, 'YB')
    assert results == expected


def test_format_as_bytes():
    utils = Utils()
    results = utils.format_bytes(size=1023, style='long')
    expected = (1023, 'bytes')
    assert results == expected


def test_format_as_long_kilobytes():
    utils = Utils()
    results = utils.format_bytes(size=765.4 * 1024, style='long')
    expected = (765.4, 'Kilobytes')
    assert results == expected


def test_format_as_long_megabytes():
    utils = Utils()
    results = utils.format_bytes(size=1.5 * 1024 ** 2, style='long')
    expected = (1.5, 'Megabytes')
    assert results == expected


def test_format_as_long_megabytes_2():
    utils = Utils()
    results = utils.format_bytes(size=9753 * 1024, style='long')
    expected = (9.5244140625, 'Megabytes')
    assert results == expected


def test_format_as_long_gigabytes():
    utils = Utils()
    results = utils.format_bytes(size=3 * 1024 ** 3, style='long')
    expected = (3.0, 'Gigabytes')
    assert results == expected


def test_format_as_long_terabytes():
    utils = Utils()
    results = utils.format_bytes(size=723 * 1024 ** 4, style='long')
    expected = (723.0, 'Terabytes')
    assert results == expected


def test_format_as_long_petabytes():
    utils = Utils()
    results = utils.format_bytes(size=1024 ** 5, style='long')
    expected = (1.0, 'Petabytes')
    assert results == expected


def test_format_as_long_exabytes():
    utils = Utils()
    results = utils.format_bytes(size=1024 ** 6, style='long')
    expected = (1.0, 'Exabytes')
    assert results == expected


def test_format_as_long_yottabytes():
    utils = Utils()
    results = utils.format_bytes(size=1024 ** 7, style='long')
    expected = (1.0, 'Yottabytes')
    assert results == expected
