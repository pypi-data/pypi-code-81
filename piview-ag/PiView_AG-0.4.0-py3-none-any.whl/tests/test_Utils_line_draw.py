from PiView_AG.Utils import Utils


def test_draw_no_line():
    utils = Utils()
    results = utils.draw_line(length=0)
    expected = ""
    assert results == expected


def test_draw_no_characters():
    utils = Utils()
    results = utils.draw_line(characters="1234567890", length=0)
    expected = ""
    assert results == expected


def test_draw_line_ten_spaces():
    utils = Utils()
    results = utils.draw_line(characters=" ", length=10)
    expected = "          "
    assert results == expected


def test_draw_line_ten_dashes():
    utils = Utils()
    results = utils.draw_line(characters="-", length=10)
    expected = "----------"
    assert results == expected


def test_draw_line_eleven_dash_dots():
    utils = Utils()
    results = utils.draw_line(characters="-.", length=11)
    expected = "-.-.-.-.-.-"
    assert results == expected


def test_draw_line_two_characters_from_six():
    utils = Utils()
    results = utils.draw_line(characters="123456", length=2)
    expected = "12"
    assert results == expected


def test_draw_default_line():
    utils = Utils()
    results = utils.draw_line()
    expected = "-=--=--=--=--=--=--=--=--=--=--=--=--=--"
    assert results == expected
