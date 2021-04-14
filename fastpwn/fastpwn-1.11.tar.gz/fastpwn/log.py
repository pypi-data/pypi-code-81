#!/usr/bin/env python3
from sys import stdout
# style ; 0-8
# range ; 30-38
# bg    ; 40-48
write=stdout.write
class c:
    h = '\033[95m'
    b = '\033[94m'
    cy = '\033[96m'
    gre = '\033[92m'
    warn = '\033[93m'
    fail = '\033[91m'
    reset = '\033[0m'
    bold = '\033[1m'
    und = '\033[4m'
def demo():
    for style in range(8):
        for fg in range(30, 38):
            fmt=';'.join([str(style), str(fg)])
            write("\x1b[%sm testing \x1b[0m : %s " % (fmt, fmt))
        write('\n')
def log(s):
    write("[%s+%s] %s%s%s [%s+%s]"%(c.warn,c.reset, c.cy,s,c.reset, c.warn,c.reset))
def warning(s):
	write()