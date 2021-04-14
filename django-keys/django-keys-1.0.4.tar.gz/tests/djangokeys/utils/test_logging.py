#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains tests for functionality to log information.

from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import MagicMock

import djangokeys.utils.logging as m


def test__log_debug():
    """ Debugging information should be logged correctly.
    """
    mock_logger = Mock()
    mock_logger.debug = MagicMock()
    with patch('djangokeys.utils.logging.getLogger') as p:
        p.return_value = mock_logger
        m.debug("hello world!")
    mock_logger.debug.assert_called_once_with("hello world!")


def test__log_info():
    """ General information should be logged correctly.
    """
    mock_logger = Mock()
    mock_logger.info = MagicMock()
    with patch('djangokeys.utils.logging.getLogger') as p:
        p.return_value = mock_logger
        m.info("hello world!")
    mock_logger.info.assert_called_once_with("hello world!")


def test__log_warning():
    """ Warnings should be logged correctly.
    """
    mock_logger = Mock()
    mock_logger.warning = MagicMock()
    with patch('djangokeys.utils.logging.getLogger') as p:
        p.return_value = mock_logger
        m.warning("hello world!")
    mock_logger.warning.assert_called_once_with("hello world!")


def test__log_error():
    """ Errors should be logged correctly.
    """
    mock_logger = Mock()
    mock_logger.error = MagicMock()
    with patch('djangokeys.utils.logging.getLogger') as p:
        p.return_value = mock_logger
        m.error("hello world!")
    mock_logger.error.assert_called_once_with("hello world!")


def test__log_critical():
    """ Critical problems should be logged correctly.
    """
    mock_logger = Mock()
    mock_logger.critical = MagicMock()
    with patch('djangokeys.utils.logging.getLogger') as p:
        p.return_value = mock_logger
        m.critical("hello world!")
    mock_logger.critical.assert_called_once_with("hello world!")
