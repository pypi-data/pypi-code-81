# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CIS UCT Prague.
#
# CIS theses repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration."""

from __future__ import absolute_import, print_function

from functools import partial

from invenio_records_rest.utils import allow_all, deny_all
from nr_common.search import community_search_factory
from oarepo_communities.links import community_record_links_factory
from oarepo_records_draft import DRAFT_IMPORTANT_FILTERS
from oarepo_records_draft.rest import DRAFT_IMPORTANT_FACETS

from nr_generic.config import FACETS, CURATOR_FACETS, CURATOR_FILTERS, FILTERS

from nr_theses.constants import PUBLISHED_THESIS_PID_TYPE, PUBLISHED_THESIS_RECORD, published_index_name, \
    DRAFT_THESIS_PID_TYPE, DRAFT_THESIS_RECORD, ALL_THESES_RECORD_CLASS, ALL_THESES_PID_TYPE, all_theses_index_name
from nr_theses.record import draft_index_name
from oarepo_multilingual import language_aware_text_term_facet, language_aware_text_terms_filter
from oarepo_ui.facets import translate_facets, term_facet
from oarepo_ui.filters import boolean_filter
from nr_common.links import nr_links_factory

from nr_theses.search import ThesisRecordSearch

_ = lambda x: x

RECORDS_DRAFT_ENDPOINTS = {
    'theses-community': {
        'draft': 'draft-theses-community',
        'pid_type': PUBLISHED_THESIS_PID_TYPE,
        'pid_minter': 'nr_theses',
        'pid_fetcher': 'nr_theses',
        'default_endpoint_prefix': True,
        'max_result_window': 500000,
        'record_class': PUBLISHED_THESIS_RECORD,
        'search_index': published_index_name,
        'search_factory_imp': community_search_factory,

        'list_route': '/<community_id>/theses/',
        'item_route': f'/<commpid({PUBLISHED_THESIS_PID_TYPE},model="theses",record_class="{PUBLISHED_THESIS_RECORD}"):pid_value>',

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
        'search_class': ThesisRecordSearch,
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
    'draft-theses-community': {
        'pid_type': DRAFT_THESIS_PID_TYPE,
        'record_class': DRAFT_THESIS_RECORD,

        'list_route': '/<community_id>/theses/draft/',
        'item_route': f'/<commpid({DRAFT_THESIS_PID_TYPE},model="theses/draft",record_class="{DRAFT_THESIS_RECORD}"):pid_value>',
        'search_index': draft_index_name,
        'links_factory_imp': partial(community_record_links_factory, original_links_factory=nr_links_factory),
        'search_factory_imp': community_search_factory,
        'search_class': ThesisRecordSearch,
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
    'theses': {
        'draft': 'draft-theses',
        'pid_type': PUBLISHED_THESIS_PID_TYPE + '-theses',
        'pid_minter': 'nr_theses',
        'pid_fetcher': 'nr_theses',
        'default_endpoint_prefix': True,
        'max_result_window': 500000,
        'record_class': ALL_THESES_RECORD_CLASS,
        'search_index': published_index_name,

        'list_route': '/theses/',
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
        'search_class': ThesisRecordSearch,
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
    'draft-theses': {
        'pid_type': DRAFT_THESIS_PID_TYPE + '-draft-theses',
        'record_class': ALL_THESES_RECORD_CLASS,

        'list_route': '/theses/draft/',
        'item_route': f'/not-really-used',
        'search_index': draft_index_name,
        'links_factory_imp': partial(community_record_links_factory, original_links_factory=nr_links_factory),
        'search_class': ThesisRecordSearch,
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
    'all-theses': dict(
        pid_type=ALL_THESES_PID_TYPE,
        pid_minter='nr_all',
        pid_fetcher='nr_all',
        default_endpoint_prefix=True,
        record_class=ALL_THESES_RECORD_CLASS,
        search_class=ThesisRecordSearch,
        search_index=all_theses_index_name,
        search_serializers={
            'application/json': 'oarepo_validate:json_search',
        },
        list_route='/theses/all/',
        links_factory_imp=partial(community_record_links_factory, original_links_factory=nr_links_factory),
        default_media_type='application/json',
        max_result_window=10000,
        # not used really
        item_route=f'/theses/'
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
    'community-theses': dict(
        pid_type=ALL_THESES_PID_TYPE + '-community-all',
        pid_minter='nr_all',
        pid_fetcher='nr_all',
        default_endpoint_prefix=True,
        record_class=ALL_THESES_RECORD_CLASS,
        search_class=ThesisRecordSearch,
        search_index=all_theses_index_name,
        search_factory_imp=community_search_factory,
        search_serializers={
            'application/json': 'oarepo_validate:json_search',
        },
        list_route='/<community_id>/theses/all/',
        links_factory_imp=partial(community_record_links_factory, original_links_factory=nr_links_factory),
        default_media_type='application/json',
        max_result_window=10000,
        # not used really
        item_route=f'/thesis/'
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


THESES_FILTERS = {
    _('defended'): boolean_filter('defended'),
    _('studyField'): language_aware_text_terms_filter('studyField.title', suffix=".keyword"),
    _('degreeGrantor'): language_aware_text_terms_filter('degreeGrantor.title', suffix=".keyword"),
    #     _('person'): terms_filter('person.keyword'),
    #     _('accessRights'): group_by_terms_filter('accessRights.title.en.raw', {
    #         "true": "open access",
    #         1: "open access",
    #         True: "open access",
    #         "1": "open access",
    #         False: ["embargoed access", "restricted access", "metadata only access"],
    #         0: ["embargoed access", "restricted access", "metadata only access"],
    #         "false": ["embargoed access", "restricted access", "metadata only access"],
    #         "0": ["embargoed access", "restricted access", "metadata only access"],
    #     }),
    #     _('resourceType'): language_aware_text_terms_filter('resourceType.title'),
    #     _('keywords'): language_aware_text_terms_filter('keywords'),
    #     _('subject'): language_aware_text_terms_filter('subjectAll'),
    #     _('language'): language_aware_text_terms_filter('language.title'),
    #     _('date'): range_filter('dateAll.date'),
    #     _('dateIssued'): range_filter('dateIssued.date'),
    #     _('dateDefended'): range_filter('dateDefended.date'),
    #     _('dateModified'): range_filter('dateModified.date'),
    #
}
#
# CURATOR_FILTERS = {
#     _('rights'): language_aware_text_terms_filter('rights.title'),
#     _('provider'): language_aware_text_terms_filter('provider.title'),
#     _('isGL'): boolean_filter('isGL')
# }
#
THESES_FACETS = {
    'defended': term_facet('defended'),
    'studyField': language_aware_text_term_facet('studyField.title', suffix=".keyword"),
    'degreeGrantor': language_aware_text_term_facet('degreeGrantor.title', suffix=".keyword"),
    # 'person': term_facet('person.keyword'),
    # 'accessRights': term_facet('accessRights.title.en.raw'),
    # 'resourceType': language_aware_text_term_facet('resourceType.title'),
    # 'keywords': language_aware_text_term_facet('keywords'),
    # 'subject': language_aware_text_term_facet('subjectAll'),
    # 'language': language_aware_text_term_facet('language.title'),
    # 'date': date_histogram_facet('dateAll.date'),
}
#
# CURATOR_FACETS = {
#     'rights': language_aware_text_term_facet('rights.title'),
#     'provider': language_aware_text_term_facet('provider.title'),
#     'dateIssued': date_histogram_facet('dateIssued.date'),
#     'dateDefended': date_histogram_facet('dateDefended.date'),
#     'dateModified': date_histogram_facet('dateModified.date'),
#     'isGL': term_facet('isGL'),
# }

RECORDS_REST_FACETS = {
    draft_index_name: {
        "aggs": translate_facets({**THESES_FACETS, **FACETS, **CURATOR_FACETS, **DRAFT_IMPORTANT_FACETS},
                                 label='{facet_key}',
                                 value='{value_key}'),
        "filters": {**THESES_FILTERS, **FILTERS, **CURATOR_FILTERS, **DRAFT_IMPORTANT_FILTERS}
    },
}

RECORDS_REST_SORT_OPTIONS = {
    draft_index_name: {
        'alphabetical': {
            'title': 'alphabetical',
            'fields': [
                'title.cs.raw'
            ],
            'default_order': 'asc',
            'order': 1
        },
        'best_match': {
            'title': 'Best match',
            'fields': ['_score'],
            'default_order': 'desc',
            'order': 1,
        }
    }
}

RECORDS_REST_DEFAULT_SORT = {
    draft_index_name: {
        'query': 'best_match',
        'noquery': 'best_match'
    }
}
