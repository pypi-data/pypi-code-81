#!/usr/bin/env python3

import sys

class PyMomRecoverableError(Exception):
    """
    A specialized exception for the PyMom framework that indicates a
    recoverable error occured in an on_message method.
    """
    pass
