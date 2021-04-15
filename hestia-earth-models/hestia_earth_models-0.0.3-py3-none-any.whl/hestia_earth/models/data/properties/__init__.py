import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.append(CURRENT_DIR)


def _load_property(filename: str):
    with open(os.path.join(CURRENT_DIR, filename)) as f:
        return f.read()
