import random

class Utils:

    def __init__(self):
        return None

    def draw_line(self, characters="-=-", length=40):
        """
        Draw a line of characters using a given character and length

        :param characters: The character(s) to draw with
        :param length: The length of the line
        :return: string
        """
        characters_length = len(characters)
        repeats = length // characters_length
        extras = length % characters_length

        line = characters * repeats

        for count in range(extras):
            next_character = characters[count]
            line = f"{line}{next_character}"

        return line

    # Original found in:
    # https://stackoverflow.com/questions/12523586/python-format-size
    # -application
    # -converting-b-to-kb-mb-gb-tb/37423778
    def format_bytes(self, size=0, style=None):
        """Formats the given value into Bytes, Kilobytes, Megabytes, ...
        Using Byte shorthand by default - B, KB, MB, ...

        The style may be:
            None | short | s  -- Short labels
            long | l          -- Long labels

        If style is anything other than above, then defaults to long format.

        :param size: integer, defaults to 0
        :param style: string, defaults to None
        :rtype: tuple
        :return: (float, string)
        """
        power = 2 ** 10  # 2**10 = 1024
        n = 0
        short_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T',
                        5: 'P', 6: 'E', 7: 'Y'}
        long_labels = {0: '', 1: 'Kilo', 2: 'Mega', 3: 'Giga',
                       4: 'Tera', 5: 'Peta', 6: 'Exa', 7: 'Yotta'}
        short_end = "B"
        long_end = "bytes"
        while size >= power:
            size /= power
            n += 1

        if style in [None, "short", 's']:
            power_labels = short_labels.copy()
            suffix = short_end
        else:
            power_labels = long_labels.copy()
            suffix = long_end

        return size, power_labels[n] + suffix


def random_percentage(min_percentage=0, max_percentage=100):
    """
    This function returns a random percentage.
    Useful for simulations when developing monitoring dashboards


    :param min_percentage: Minimum value to return, default 0.0
    :param max_percentage: Maximum to return, default 100.0
    :rtype: float
    :return: A random CPU load value between 0% and 100% to 1DP
    """
    load = random.gauss(55, 10)
    if load < min_percentage:
        return 0.0
    elif load > max_percentage:
        return 100.0
    else:
        return round(load, 1)
