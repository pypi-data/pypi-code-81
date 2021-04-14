# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CIS UCT Prague.
#
# CIS events repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration."""

from __future__ import absolute_import, print_function

from functools import partial

from invenio_records_rest.utils import allow_all, deny_all
from nr_common.search import community_search_factory
from oarepo_communities.links import community_record_links_factory

from nr_events.constants import PUBLISHED_EVENT_PID_TYPE, PUBLISHED_EVENT_RECORD, published_index_name, \
    DRAFT_EVENT_PID_TYPE, DRAFT_EVENT_RECORD, ALL_EVENTS_RECORD_CLASS, ALL_EVENTS_PID_TYPE, all_events_index_name
from nr_events.record import draft_index_name
from nr_events.search import EventsRecordsSearch
from nr_common.links import nr_links_factory


RECORDS_DRAFT_ENDPOINTS = {
    'events-community': {
        'draft': 'draft-events-community',
        'pid_type': PUBLISHED_EVENT_PID_TYPE,
        'pid_minter': 'nr_events',
        'pid_fetcher': 'nr_events',
        'default_endpoint_prefix': True,
        'max_result_window': 500000,
        'record_class': PUBLISHED_EVENT_RECORD,
        'search_index': published_index_name,
        'search_factory_imp': community_search_factory,

        'list_route': '/<community_id>/events/',
        'item_route': f'/<commpid({PUBLISHED_EVENT_PID_TYPE},model="events",record_class="{PUBLISHED_EVENT_RECORD}"):pid_value>',

        'publish_permission_factory_imp': 'nr_common.permissions.publish_draft_object_permission_impl',
        'unpublish_permission_factory_imp': 'nr_common.permissions.unpublish_draft_object_permission_impl',
        'edit_permission_factory_imp': 'nr_common.permissions.update_object_permission_impl',
        'list_permission_factory_imp': allow_all,
        'read_permission_factory_imp': allow_all,
        'create_permission_factory_imp': deny_all,
        'update_permission_factory_imp': deny_all,
        'delete_permission_factory_imp': deny_all,
        'default_media_type': 'application/json',
        'links_factory_imp': partial(community_record_links_factory, original_links_factory=nr_links_factory),
        'search_class': EventsRecordsSearch,
        # 'indexer_class': CommitingRecordIndexer,
        'files': dict(
            # Who can upload attachments to a draft dataset record
            put_file_factory=deny_all,
            # Who can download attachments from a draft dataset record
            get_file_factory=allow_all,
            # Who can delete attachments from a draft dataset record
            delete_file_factory=deny_all
        )

    },
    'draft-events-community': {
        'pid_type': DRAFT_EVENT_PID_TYPE,
        'record_class': DRAFT_EVENT_RECORD,

        'list_route': '/<community_id>/events/draft/',
        'item_route': f'/<commpid({DRAFT_EVENT_PID_TYPE},model="events/draft",record_class="{DRAFT_EVENT_RECORD}"):pid_value>',
        'search_index': draft_index_name,
        'links_factory_imp': partial(community_record_links_factory, original_links_factory=nr_links_factory),
        'search_factory_imp': community_search_factory,
        'search_class': EventsRecordsSearch,
        'search_serializers': {
            'application/json': 'oarepo_validate:json_search',
        },
        'record_serializers': {
            'application/json': 'oarepo_validate:json_response',
        },

        'create_permission_factory_imp': 'nr_common.permissions.create_draft_object_permission_impl',
        'update_permission_factory_imp': 'nr_common.permissions.update_draft_object_permission_impl',
        'read_permission_factory_imp': 'nr_common.permissions.read_draft_object_permission_impl',
        'delete_permission_factory_imp': 'nr_common.permissions.delete_draft_object_permission_impl',
        'list_permission_factory_imp': 'nr_common.permissions.list_draft_object_permission_impl',
        'record_loaders': {
            'application/json': 'oarepo_validate.json_files_loader',
            'application/json-patch+json': 'oarepo_validate.json_loader'
        },
        'files': dict(
            put_file_factory='nr_common.permissions.put_draft_file_permission_impl',
            get_file_factory='nr_common.permissions.get_draft_file_permission_impl',
            delete_file_factory='nr_common.permissions.delete_draft_file_permission_impl'
        )

    },
    'events': {
        'draft': 'draft-events',
        'pid_type': PUBLISHED_EVENT_PID_TYPE + '-events',
        'pid_minter': 'nr_events',
        'pid_fetcher': 'nr_events',
        'default_endpoint_prefix': True,
        'max_result_window': 500000,
        'record_class': ALL_EVENTS_RECORD_CLASS,
        'search_index': published_index_name,

        'list_route': '/events/',
        'item_route': f'/not-really-used',
        'publish_permission_factory_imp': deny_all,
        'unpublish_permission_factory_imp': deny_all,
        'edit_permission_factory_imp': deny_all,
        'list_permission_factory_imp': allow_all,
        'read_permission_factory_imp': allow_all,
        'create_permission_factory_imp': deny_all,
        'update_permission_factory_imp': deny_all,
        'delete_permission_factory_imp': deny_all,
        'default_media_type': 'application/json',
        'links_factory_imp': partial(community_record_links_factory, original_links_factory=nr_links_factory),
        'search_class': EventsRecordsSearch,
        # 'indexer_class': CommitingRecordIndexer,
        'files': dict(
            # Who can upload attachments to a draft dataset record
            put_file_factory=deny_all,
            # Who can download attachments from a draft dataset record
            get_file_factory=allow_all,
            # Who can delete attachments from a draft dataset record
            delete_file_factory=deny_all
        )
    },
    'draft-events': {
        'pid_type': DRAFT_EVENT_PID_TYPE + '-draft-events',
        'record_class': ALL_EVENTS_RECORD_CLASS,

        'list_route': '/events/draft/',
        'item_route': f'/not-really-used',
        'search_index': draft_index_name,
        'links_factory_imp': partial(community_record_links_factory, original_links_factory=nr_links_factory),
        'search_class': EventsRecordsSearch,
        'search_serializers': {
            'application/json': 'oarepo_validate:json_search',
        },
        'record_serializers': {
            'application/json': 'oarepo_validate:json_response',
        },

        'create_permission_factory_imp': deny_all,
        'update_permission_factory_imp': deny_all,
        'read_permission_factory_imp': 'nr_common.permissions.read_draft_object_permission_impl',
        'delete_permission_factory_imp': deny_all,
        'list_permission_factory_imp': 'nr_common.permissions.list_draft_object_permission_impl',
        'files': dict(
            put_file_factory=deny_all,
            get_file_factory='nr_common.permissions.get_draft_file_permission_impl',
            delete_file_factory=deny_all
        )
    }
}


RECORDS_REST_ENDPOINTS = {
    'all-events': dict(
        pid_type=ALL_EVENTS_PID_TYPE,
        pid_minter='nr_all',
        pid_fetcher='nr_all',
        default_endpoint_prefix=True,
        record_class=ALL_EVENTS_RECORD_CLASS,
        search_class=EventsRecordsSearch,
        search_index=all_events_index_name,
        search_serializers={
            'application/json': 'oarepo_validate:json_search',
        },
        list_route='/events/all/',
        links_factory_imp=partial(community_record_links_factory, original_links_factory=nr_links_factory),
        default_media_type='application/json',
        max_result_window=10000,
        # not used really
        item_route=f'/events/'
                   f'/not-used-but-must-be-present',
        list_permission_factory_imp='nr_common.permissions.list_all_object_permission_impl',
        create_permission_factory_imp=deny_all,
        delete_permission_factory_imp=deny_all,
        update_permission_factory_imp=deny_all,
        read_permission_factory_imp=deny_all,
        record_serializers={
            'application/json': 'oarepo_validate:json_response',
        },
        use_options_view=False
    ),
    'community-events': dict(
        pid_type=ALL_EVENTS_PID_TYPE + '-community-all',
        pid_minter='nr_all',
        pid_fetcher='nr_all',
        default_endpoint_prefix=True,
        record_class=ALL_EVENTS_RECORD_CLASS,
        search_class=EventsRecordsSearch,
        search_index=all_events_index_name,
        search_factory_imp=community_search_factory,
        search_serializers={
            'application/json': 'oarepo_validate:json_search',
        },
        list_route='/<community_id>/events/all/',
        links_factory_imp=partial(community_record_links_factory, original_links_factory=nr_links_factory),
        default_media_type='application/json',
        max_result_window=10000,
        # not used really
        item_route=f'/event/'
                   f'/not-used-but-must-be-present',
        list_permission_factory_imp='nr_common.permissions.list_all_object_permission_impl',
        create_permission_factory_imp=deny_all,
        delete_permission_factory_imp=deny_all,
        update_permission_factory_imp=deny_all,
        read_permission_factory_imp=deny_all,
        record_serializers={
            'application/json': 'oarepo_validate:json_response',
        },
        use_options_view=False
    )
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
