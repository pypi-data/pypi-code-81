"""Collection of nodes used in unittests.

PYTHONPATH will be automatically set so Python can find this package.
"""
import sys
import argparse


def hello(argv, *, stdin=None, stdout=None, stderr=None):
    parser = argparse.ArgumentParser("hello")
    parser.add_argument("name", type=str, help="your name")
    args = parser.parse_args(argv[1:])

    # Write to sys.stdout or to provided output stream (for pymodule)
    print(f"hello {args.name} !", file=stdout if stdout is not None else sys.stdout)


if __name__ == "__main__":
    hello(sys.argv)
