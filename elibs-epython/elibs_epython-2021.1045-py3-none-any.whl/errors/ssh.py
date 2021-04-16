# -*- coding: utf-8 -*-
"""
Description:
    This module contains the ssh exceptions used for epython.

Author:
    Ray Gomez

Date:
    12/7/20
"""

from epython.errors.base import EPythonException


class SSHError(EPythonException):
    """ A generic SSH Failure. """


class SSHKeyNotFound(SSHError):
    """ Failure when an ssh key isn't found at a specified location. """


class SSHStreamDecodeError(SSHError):
    """ Failure when there is an issue decoding the stdout or stderr. """


class SSHTimeoutError(SSHError):
    """ Failure when an SSH Connection times out. """
