import sys
import time


def h_print(text, time_=0.3):
    if time_ is not None:
        sys.stdout.write("\r " + " " * 60 + "\r")
        sys.stdout.flush()
        for c in text:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(time_)

