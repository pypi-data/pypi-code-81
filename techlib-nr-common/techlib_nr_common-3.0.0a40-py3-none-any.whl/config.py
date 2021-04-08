# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CIS UCT Prague.
#
# CIS theses repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration."""

from __future__ import absolute_import, print_function

from invenio_records_rest.facets import terms_filter, range_filter
from invenio_records_rest.utils import allow_all
from oarepo_communities.links import community_record_links_factory
from oarepo_communities.search import CommunitySearch
from oarepo_records_draft.rest import term_facet, DRAFT_IMPORTANT_FILTERS, DRAFT_IMPORTANT_FACETS

from nr_common.constants import PUBLISHED_COMMON_PID_TYPE, PUBLISHED_COMMON_RECORD, \
    DRAFT_COMMON_PID_TYPE, DRAFT_COMMON_RECORD
from nr_common.record import published_index_name, draft_index_name
from oarepo_multilingual import language_aware_text_term_facet, \
    language_aware_text_terms_filter
from oarepo_ui.facets import date_histogram_facet, translate_facets
from oarepo_ui.filters import group_by_terms_filter, boolean_filter



_ = lambda x: x

RECORDS_DRAFT_ENDPOINTS = {
    'common': {
        'draft': 'draft-common',
        'pid_type': PUBLISHED_COMMON_PID_TYPE,
        'pid_minter': 'nr_common',
        'pid_fetcher': 'nr_common',
        'default_endpoint_prefix': True,
        'max_result_window': 500000,
        'record_class': PUBLISHED_COMMON_RECORD,
        # TODO: doplnit indexer class
        'list_route': '/common/',
        'item_route': '/common/',
        'publish_permission_factory_imp': allow_all,  # TODO: change this !!!
        'unpublish_permission_factory_imp': allow_all,
        'edit_permission_factory_imp': allow_all,
        'default_media_type': 'application/json',
        'search_index': published_index_name,
        'links_factory_imp': community_record_links_factory,
        'search_class': CommunitySearch
    },
    'draft-common': {
        'pid_type': DRAFT_COMMON_PID_TYPE,
        'record_class': DRAFT_COMMON_RECORD,
        'list_route': '/draft/common/',
        'item_route': '/draft/common/',
        'search_index': draft_index_name,
        'links_factory_imp': community_record_links_factory,
        'search_class': CommunitySearch
    }
}

ELASTICSEARCH_LANGUAGE_TEMPLATES = {
    "*#subjectAll": {
        "type": "text",
        "copy_to": "subjectAll.*",
        "fields": {
            "raw": {
                "type": "keyword"
            }
        }
    }

}

FILTERS = {
    _('person'): terms_filter('person.keyword'),
    _('accessRights'): group_by_terms_filter('accessRights.title.en.raw', {
        "true": "open access",
        1: "open access",
        True: "open access",
        "1": "open access",
        False: ["embargoed access", "restricted access", "metadata only access"],
        0: ["embargoed access", "restricted access", "metadata only access"],
        "false": ["embargoed access", "restricted access", "metadata only access"],
        "0": ["embargoed access", "restricted access", "metadata only access"],
    }),
    _('resourceType'): language_aware_text_terms_filter('resourceType.title'),
    _('keywords'): language_aware_text_terms_filter('keywords'),
    _('subject'): language_aware_text_terms_filter('subjectAll'),
    _('language'): language_aware_text_terms_filter('language.title'),
    _('date'): range_filter('dateAll.date'),
    _('dateIssued'): range_filter('dateIssued.date'),
    _('dateDefended'): range_filter('dateDefended.date'),
    _('dateModified'): range_filter('dateModified.date'),
}

CURATOR_FILTERS = {
    _('accessRightsCurator'): language_aware_text_terms_filter('accessRights.title'),
    _('rights'): language_aware_text_terms_filter('rights.title'),
    _('provider'): language_aware_text_terms_filter('provider.title'),
    _('entities'): language_aware_text_terms_filter('entities.title'),
    _('isGL'): boolean_filter('isGL')
}

FACETS = {
    'person': term_facet('person.keyword'),
    'accessRights': term_facet('accessRights.title.en.raw'),
    'resourceType': language_aware_text_term_facet('resourceType.title'),
    'keywords': language_aware_text_term_facet('keywords'),
    'subject': language_aware_text_term_facet('subjectAll'),
    'language': language_aware_text_term_facet('language.title'),
    'date': date_histogram_facet('dateAll.date'),
}

CURATOR_FACETS = {
    'rights': language_aware_text_term_facet('rights.title'),
    'provider': language_aware_text_term_facet('provider.title'),
    'entities': language_aware_text_term_facet('entities.title'),
    'dateIssued': date_histogram_facet('dateIssued.date'),
    'dateDefended': date_histogram_facet('dateDefended.date'),
    'dateModified': date_histogram_facet('dateModified.date'),
    'isGL': term_facet('isGL'),
    'accessRightsCurator': language_aware_text_term_facet('accessRights.title')
}

# def degree_grantor_filter(field, path=None):
#     def inner(values):
#         return Q('nested',
#                  path="degreeGrantor.ancestors",
#                  query=Q("nested",
#                          path="degreeGrantor.ancestors.title",
#                          query=Q('terms',
#                                  **{field: values}
#                                  ))
#                  )
#
#     return inner

#
# def nested_terms_filter(prefix, field, field_query=None):
#     """Create a term filter.
#
#     :param prefix
#     :param field: Field name.
#     :param field_query
#     :returns: Function that returns the Terms query.
#     """
#
#     field = prefix + '.' + field
#
#     def inner(values):
#         if field_query:
#             query = field_query(field)(values)
#         else:
#             query = Q('terms', **{field: values})
#         return Q('nested', path=prefix, query=query)
#
#     return inner


# def year_filter(field):
#     """Create a term filter.
#
#     :param field: Field name.
#     :returns: Function that returns the Terms query.
#     """
#
#     def inner(values):
#         queries = []
#         for value in values:
#             queries.append(
#                 Q('range', **{
#                     field: {
#                         "gte": value,
#                         "lt": int(value) + 1,
#                         "format": "yyyy"
#                     }
#                 })
#             )
#         return Q('bool', should=queries, minimum_should_match=1)
#
#     return inner


# def person_filter(field):
#     """Create a term filter.
#
#     :param field: Field name.
#     :returns: Function that returns the Terms query.
#     """
#
#     def inner(values):
#         queries = []
#         for value in values:
#             queries.append(
#                 Q('term', **{
#                     field: value
#                 })
#             )
#         return Q('bool', should=queries, minimum_should_match=1)
#
#     return inner
#
#
# def boolean_filter(field):
#     def inner(values):
#         queries = []
#         for value in values:
#             queries.append(
#                 Q('term', **{
#                     field: bool(int(value))
#                 })
#             )
#         return Q('bool', should=queries, minimum_should_match=1)
#
#     return inner


RECORDS_REST_FACETS = {
    draft_index_name: {
        "aggs": translate_facets({**FACETS, **CURATOR_FACETS, **DRAFT_IMPORTANT_FACETS},
                                 label='{facet_key}',
                                 value='{value_key}'),
        "filters": {**FILTERS, **CURATOR_FILTERS, **DRAFT_IMPORTANT_FILTERS}
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

"""Set default sorting options."""
