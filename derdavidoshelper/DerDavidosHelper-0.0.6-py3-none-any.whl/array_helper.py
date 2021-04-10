from DerDavidosHelper import custom_print as cp


def print_array(array, name="", new_line=False, number=True):
    """
    prints all element of an array
    :param array: array to print
    :param name: Name of Array
    :param number: number each element
    :param new_line: Write end line aftere each element
    """

    length = len(array)

    if len(name) > 0:
        wrap = cp.custom_print(cp.PT.RED, "----- ", cp.PT.BOLD, name, cp.PT.RESET, cp.PT.RED, " -----",
                               return_string=True)
    else:
        wrap = cp.custom_print(cp.PT.RED, "----- Array -----", return_string=True)

    cp.custom_print(wrap)
    cp.custom_print(cp.PT.BLUE, "Length:", length)
    for i, x in enumerate(array, start=0):
        if number:
            cp.custom_print(cp.PT.GREY, i, ":", sep="", new_line=False)
        if i < length - 1:
            cp.custom_print(cp.PT.GREEN, x, sep="", end=", ", new_line=new_line)
        else:
            cp.custom_print(cp.PT.GREEN, x, sep="")
    cp.custom_print(wrap)


pa = print_array
