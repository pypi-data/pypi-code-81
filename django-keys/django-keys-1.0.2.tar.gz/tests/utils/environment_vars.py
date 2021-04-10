#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains a context manager for temporarily introducing an environment var.

import os
import contextlib


@contextlib.contextmanager
def use_environment_variable(key, value):
    """ Used to temporarily introduce a new environment variable as if it
        was set by the execution environment.

    :param str key: key of environment variable
    :param str value: value of environment variable
    """
    assert type(value) == str
    assert key not in os.environ
    os.environ[key] = value
    assert key in os.environ
    yield
    assert key in os.environ
    os.environ.pop(key)
    assert key not in os.environ
