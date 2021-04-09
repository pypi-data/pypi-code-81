def find_all(string, sub_string, tuples=False):
    """
    Finds all postions of substing
    :param str string: string to find in
    :param str sub_string: sub string to find in string
    :param bool tuples: if only return start postions or end and start in a tuple
    :return array: positions of sub string in string
    """
    l = len(sub_string)
    positions = []
    start = 0
    while True:
        pos = string.find(sub_string)
        if pos == -1:
            return positions

        if tuples:
            positions.append((start + pos, start + pos + l))
        else:
            positions.append(start + pos)

        start += pos + 1
        string = string[pos + 1:]

fa = find_all
