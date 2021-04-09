# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CIS UCT Prague.
#
# CIS theses repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration."""

from __future__ import absolute_import, print_function

from invenio_records_rest.utils import allow_all

from nr_events.record import draft_index_name

RECORDS_DRAFT_ENDPOINTS = {
    'events': {
        'draft': 'draft-events',

        'pid_type': 'nrevt',
        'pid_minter': 'nr_events',
        'pid_fetcher': 'nr_events',
        'default_endpoint_prefix': True,
        'max_result_window': 500000,
        'record_class': 'nr_events.record:PublishedEventRecord',
        'list_route': '/events/',
        'publish_permission_factory_imp': allow_all,  # TODO: change this !!!
        'unpublish_permission_factory_imp': allow_all,
        'edit_permission_factory_imp': allow_all,
        'default_media_type': 'application/json',
        'links_factory_imp': 'oarepo_fsm.links:record_fsm_links_factory'
        # 'indexer_class': CommitingRecordIndexer,

    },
    'draft-events': {
        'pid_type': 'dnrevt',
        'record_class': 'nr_events.record:DraftEventRecord',
        'list_route': '/draft/events/',
        'search_index': draft_index_name,
        'links_factory_imp': 'oarepo_fsm.links:record_fsm_links_factory'
    }
}

FILTERS = {
}

POST_FILTERS = {
}

RECORDS_REST_FACETS = {
}

RECORDS_REST_SORT_OPTIONS = {
}

RECORDS_REST_DEFAULT_SORT = {
}

"""Set default sorting options."""
