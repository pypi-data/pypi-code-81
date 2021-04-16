#!/usr/bin/env python3

import sys

class PyMomUnrecoverableError(Exception):
    """
    A specialized exception for the PyMom framework that indicates an
    unrecoverable error occured in an on_message method.
    """
    pass
