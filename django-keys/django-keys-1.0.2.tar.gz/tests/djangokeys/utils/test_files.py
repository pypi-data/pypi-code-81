#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains tests for functionality to interact with files.

from unittest.mock import patch
from unittest.mock import MagicMock

import pytest

import djangokeys.utils.files as m


def test__touch_file__file_exists():
    """ A file isn't touched when it already exists.
    """
    with patch('djangokeys.utils.files.open') as mock:
        m.touch_file(__file__)
    mock.assert_not_called()


def test__touch_file__file_doesnt_exist():
    """ A file is created when it doesn't exist yet.
    """
    with patch('djangokeys.utils.files.open') as mock:
        mock.return_value = MagicMock()
        m.touch_file('./does/not/exist')
    mock.assert_called_once_with('./does/not/exist', 'w')
    mock.return_value.close.assert_called_once_with()


def test__touch_file__cannot_create():
    """ An appropriate exception is raised when file cannot be created.
    """
    with patch('djangokeys.utils.files.open') as mock:
        mock.side_effect = IOError("oops")
        with pytest.raises(m.CouldNotCreateFile):
            m.touch_file('/also/does/not/exist')
    mock.assert_called_once_with('/also/does/not/exist', 'w')
