#!/usr/bin/env python3
from sys import argv
path="/proc/sys/kernel/randomize_va_space"
def write(n):
    with open(path, "w") as f:
        f.write(n)
        f.close()
def read():
    with open(path, "r") as f:
        return True if int(f.read())==0 else False
        f.close()
if __name__ == "__main__":
    try:
        if len(argv)>1 and argv[1]=="-n":
            write("0")
            print("done!")
        elif argv[1] == "-c":
            if read():
                print("Aslr is disabled")
            else:
                print("Aslr is enabled")
        elif argv[1]=="-w":
            try:
                write(argv[2])
                print("done!")
            except IndexError:
                print("Error: Must provide integer to write!\nExample: aslr -w 1")
    except IndexError:
        print("Usage: aslr [-n] [-c] [-w]")
        print("-n\tturn off aslr\n-c\tcheck if aslr is enabled\n-w \twrite custom integer to aslr")
