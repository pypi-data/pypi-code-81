#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Used to create logs for djangokeys.

from logging import getLogger


def debug(msg):
    """ Used to log information that is only helpful during development.

    :param str msg: log message
    """
    logger = getLogger('djangokeys')
    logger.debug(msg)


def info(msg):
    """ Used to log information that is helpful during regular operation.

    :param str msg: log message
    """
    logger = getLogger('djangokeys')
    logger.info(msg)


def warning(msg):
    """ Used to log potential problems or minor problems.

    :param str msg: log message
    """
    logger = getLogger('djangokeys')
    logger.warning(msg)


def error(msg):
    """ Used to log major problems.

    :param str msg: log message
    """
    logger = getLogger('djangokeys')
    logger.error(msg)


def critical(msg):
    """ Used to critical problems.

    :param str msg: log message
    """
    logger = getLogger('djangokeys')
    logger.critical(msg)
