# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CIS UCT Prague.
#
# CIS theses repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Flask extension for CIS theses repository."""

from __future__ import absolute_import, print_function

import logging

from . import config

log = logging.getLogger('nr-theses')


class NRTheses(object):
    """CIS theses repository extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)

    def init_config(self, app):
        """Initialize configuration.

        Override configuration variables with the values in this package.
        """
        app.config.setdefault('RECORDS_DRAFT_ENDPOINTS', {}).update(config.RECORDS_DRAFT_ENDPOINTS)
        app.config.setdefault('RECORDS_REST_ENDPOINTS', {}).update(config.RECORDS_REST_ENDPOINTS)
        app.config.setdefault('RECORDS_REST_FACETS', {}).update(config.RECORDS_REST_FACETS)

        app.config.setdefault('RECORDS_REST_SORT_OPTIONS', {}).update(
            config.RECORDS_REST_SORT_OPTIONS)

        app.config.setdefault('RECORDS_REST_DEFAULT_SORT', {}).update(
            config.RECORDS_REST_DEFAULT_SORT)
