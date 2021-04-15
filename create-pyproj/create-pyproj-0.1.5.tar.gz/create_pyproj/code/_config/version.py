# -*- coding: utf-8 -*-
"""
Module Description.


"""
from pathlib import Path

DIR = Path(__file__).parent.absolute()


def getVersion():
    with open(DIR.parent.parent / 'VERSION', 'r') as f:
        VERSION = f.read().strip()
    return VERSION


