from DerDavidosHelper import cprint as cp

def print_array(array, name="", new_line=False, number=True):
    """
    prints all element of an array
    :param array: array to print
    :param name: Name of Array
    :param number: number each element
    :param new_line: Write end line aftere each element
    """

    l = len(array)
    cp.cprint(cp.PT.RED, "----- Array", cp.PT.BOLD, name, cp.PT.RESET, cp.PT.RED, "print -----")
    cp.cprint(cp.PT.BLUE, "Length:", l)
    for i, x in enumerate(array, start=0):
        if number:
            cp.cprint(cp.PT.GREY, i, ":", sep="", new_line=False)
        if i < l - 1:
            cp.cprint(cp.PT.GREEN, x, sep="", end=", ", new_line=new_line)
        else:
            cp.cprint(cp.PT.GREEN, x, sep="")
    cp.cprint(cp.PT.RED, "----- Array", cp.PT.BOLD, name, cp.PT.RESET, cp.PT.RED, "print -----")

pa = print_array