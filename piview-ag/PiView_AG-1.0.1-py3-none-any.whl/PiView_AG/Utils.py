# Project:    PiView
# Filename:   Utils.py
# Location:   ./PiView_AG
# Author:     Adrian Gould <adrian.gould@nmtafe.wa.edu.au>
# Created:    10/04/21
#
# This file provides the following features, methods and associated
# supporting code:
# - draw a line using a provided string
# - format a number (bytes) into Bytes, KB, MB, GB,...
# - random number (percentage) between max and min percentages

import random


class Utils:
    @staticmethod
    def draw_line(characters="-=-", length=40):
        """
        Draw a line of characters using a given character and length

        :param characters: string, the character(s) to draw with
        :param length: integer), the length of the line
        :rtype: string
        :return: A string of exactly length characters
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
    @staticmethod
    def format_bytes(size=0, style=None):
        """
        Formats the given value into Bytes, Kilobytes, Megabytes, ...

        Using Byte shorthand by default - B, KB, MB, ...

        The style may be:

        - None | short | s  -- Short labels
        - long | l          -- Long labels

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

    @staticmethod
    def random_percentage(min_percentage=0, max_percentage=100):
        """
        This function returns a random percentage.
        Useful for simulations when developing monitoring dashboards


        :param min_percentage: float, minimum value to return, default 0.0
        :param max_percentage: float, maximum to return, default 100.0
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
