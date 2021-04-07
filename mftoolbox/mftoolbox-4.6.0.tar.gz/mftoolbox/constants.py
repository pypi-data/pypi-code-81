class Color:
    __escape_code__ = '\033[{}m'

    #light fore colors
    red = __escape_code__.format(91)
    green = __escape_code__.format(92)
    yellow = __escape_code__.format(93)
    blue = __escape_code__.format(94)
    purple = __escape_code__.format(95)
    cyan = __escape_code__.format(96)
    white = __escape_code__.format(97)
    grey = __escape_code__.format(37)

    #dark fore colors
    dark_red = __escape_code__.format(31)
    dark_green = __escape_code__.format(32)
    dark_yellow = __escape_code__.format(33)
    dark_blue = __escape_code__.format(34)
    dark_purple = __escape_code__.format(35)
    dark_cyan = __escape_code__.format(36)

    #effects
    end = __escape_code__.format(0)
    bold = __escape_code__.format(1)
    italic = __escape_code__.format(3)
    underline = __escape_code__.format(4)
    strong_underline = __escape_code__.format(21)
    striketrough = __escape_code__.format(9)
    black_box = __escape_code__.format(51)

    #backgrounds
    black_background_white_front = __escape_code__.format(7)
    black_background = __escape_code__.format(40)
    dark_red_background = __escape_code__.format(41)
    dark_green_background = __escape_code__.format(42)
    dark_yellow_background = __escape_code__.format(43)
    dark_blue_background = __escape_code__.format(44)
    dark_purple_background = __escape_code__.format(45)
    dark_cyan_background = __escape_code__.format(46)
    dark_grey_background = __escape_code__.format(47)
    grey_background = __escape_code__.format(100)
    red_background = __escape_code__.format(101)
    green_background = __escape_code__.format(102)
    yellow_background = __escape_code__.format(103)
    blue_background = __escape_code__.format(104)
    purple_background = __escape_code__.format(105)
    cyan_background = __escape_code__.format(106)


class Header:

    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
              'Cache-Control': 'no-cache',
              'referer':'https://www.google.com/'}