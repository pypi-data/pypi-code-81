import sys
debug = True
def dprint(msg):
    msg = f"DEBUG: {msg}\n"
    if debug:
        sys.stderr.write(msg)
if __name__ == "__main__":
    dprint("this is an error")
