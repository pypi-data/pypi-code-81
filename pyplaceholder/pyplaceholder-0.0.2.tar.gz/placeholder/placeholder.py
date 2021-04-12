from typing import Tuple, List


def parse_placeholders(text: str, open_ch: str = '{', close_ch: str = '}',
                       escapes: bool = True) -> Tuple[str, List[Tuple[int, int]]]:
    """ Parse a text in order to detect placeholders based on an open and a close characters. It is possible to use
    escape sequences with the character \\. For example, if we have the following text::

       s = 'Some example of {Entity} \\\\{EUTM\\\\}'

    And it is parsed::

      parse_place_holders(s)

    The following tuple is obtained::

      ('Some example of {Terms:Entity} {EUTM}', [(16, 30)])

    Or if it is parsed this text::

      s = 'Some example of {Terms:Entity} \\\\\\\\\\\\{EUTM\\\\\\\\\\\\}\\\\ {Intent:definition}'

    We will get::

      ('Some example of {Terms:Entity} \\\\{EUTM}\\\\ {Intent:definition}', [(16, 30), (41, 60)])

    :param text: The text to parse.
    :param open_ch: The character which marks the placeholder init.
    :param close_ch: The character which marks the placeholder end.
    :param escapes: True if the escapes must be escaped from the final text or not. False does not change the final
       text and the positions will be not modified consequently.
    :return: A tuple with a new text with the escape sequences parsed and a list of position of placeholders.
    :raises ValueError: If the open and close characters have a length different to 1.
    """
    if len(open_ch) != 1 or len(close_ch) != 1:
        raise ValueError('The open and close characters must be just one character.')
    if open_ch == '\\' or close_ch == '\\':
        raise ValueError('Neither, open or close parameters, can contain the \\ as delimiter character.')
    pos = []
    i, ini = 0, -1
    while i < len(text):
        c = text[i]
        if c == '\\' and i < len(text) - 1 and text[i + 1] in ['\\', open_ch, close_ch]:
            if escapes:
                text = text[:i] + text[i + 1:]
            else:
                i += 1
        elif c == open_ch and ini == -1:
            ini = i
        elif c == close_ch and ini != -1:
            pos.append((ini, i + 1))
            ini = -1
        i += 1
    return text, pos


def num_placeholders(text: str, open_ch: str = '{', close_ch: str = '}') -> int:
    """ Count the placeholders in a text taking into account the escape sequences.
    :param text: The text to count the placeholders.
    :param open_ch: The character which marks the placeholder init.
    :param close_ch: The character which marks the placeholder end.
    :return: The number of placeholders.
    :raises ValueError: If the open and close characters have a length different to 1.
    """
    result = parse_placeholders(text, open_ch, close_ch, True)
    return len(result[1])


def has_placeholders(text: str, open_ch: str = '{', close_ch: str = '}') -> bool:
    """
    Check if a text has, at least, a placeholder taking into account the escape sequences.
    :param text: The text to detect the placeholders.
    :param open_ch: The character which marks the placeholder init.
    :param close_ch: The character which marks the placeholder end.
    :return: True if the text contains placeholders, otherwise False.
    :raises ValueError: If the open and close characters have a length different to 1.
    """
    return bool(num_placeholders(text, open_ch, close_ch))


def replace_placeholders(text: str, open_ch: str = '{', close_ch: str = '}', **kwargs) -> str:
    """ Replace placeholders for its references. For example, if we have the following text::

      s = 'Some example of {entity} \\\\\\\\\\\\{EUTM\\\\\\\\\\\\}\\\\ {intent}'

    And we execute::

      replace_placeholders(s, entity='car', intent='definition')

    The result will be::

      'Some example of car \\\\{EUTM\\\\}\\\\ definition'

    :param text: The text with the placeholders.
    :param open_ch: The character which marks the placeholder init.
    :param close_ch: The character which marks the placeholder end.
    :param kwargs: Extra arguments with the referenced data in the placeholders.
    :return: The replaced text without placeholders.
    :raises KeyError: If a reference is not in the kwargs.
    """
    text, positions = parse_placeholders(text, open_ch, close_ch)
    for pos in reversed(positions):
        ref = text[pos[0] + 1:pos[1] - 1]
        text = text[:pos[0]] + kwargs[ref] + text[pos[1]:]
    return text


def replace_file_placeholders(input_file: str, output_file: str,
                              open_ch: str = '{', close_ch: str = '}', **kwargs) -> None:
    """ Replace the placeholders in a text file.
    :param input_file: The text file path to read.
    :param output_file: The output file path to write.
    :param open_ch: The character which marks the placeholder init.
    :param close_ch: The character which marks the placeholder end.
    :param kwargs: Extra arguments with the referenced data in the placeholders.
    """
    with open(input_file, 'rt') as input_file:
        with open(output_file, 'wt') as output_file:
            for line in input_file:
                if has_placeholders(line, open_ch, close_ch):
                    line = replace_placeholders(line, open_ch, close_ch, **kwargs)
                output_file.write(line)
