# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CIS UCT Prague.
#
# CIS theses repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration."""

from __future__ import absolute_import, print_function

from invenio_records_rest.utils import allow_all

from nr_nresults.record import draft_index_name, published_index_name
from nr_nresults.search import NresultsRecordsSearch

RECORDS_DRAFT_ENDPOINTS = {
    'nresults': {
        'draft': 'draft-nresults',

        'pid_type': 'nrnrs',
        'pid_minter': 'nr_nresults',
        'pid_fetcher': 'nr_nresults',
        'default_endpoint_prefix': True,
        'max_result_window': 500000,
        'search_index': published_index_name,  # TODO: nestáhl se sám, podívat se na to
        'record_class': 'nr_nresults.record:PublishedNResultRecord',
        'list_route': '/nresults/',
        'publish_permission_factory_imp': allow_all,  # TODO: change this !!!
        'unpublish_permission_factory_imp': allow_all,
        'edit_permission_factory_imp': allow_all,
        'default_media_type': 'application/json',
        'links_factory_imp': 'oarepo_fsm.links:record_fsm_links_factory',
        'search_class': NresultsRecordsSearch
        # 'indexer_class': CommitingRecordIndexer,

    },
    'draft-nresults': {
        'pid_type': 'dnrnrs',
        'record_class': 'nr_nresults.record.DraftNResultRecord',
        'list_route': '/draft/nresults/',
        'search_index': draft_index_name,
        'links_factory_imp': 'oarepo_fsm.links:record_fsm_links_factory',
        'search_class': NresultsRecordsSearch
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
