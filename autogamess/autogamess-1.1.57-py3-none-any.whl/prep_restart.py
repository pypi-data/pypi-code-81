from .config import *

def prep_restart(inpfile, rstfile):
    """

    """
    vib = '$VIB2'

    rst = read_file(rstfile)

    i = ctr_f(rst, vib)

    with open(inpfile, 'a') as f:
        f.write(rst[i:])

    return
