import functools
import re

from boltons.typeutils import classproperty
from elasticsearch_dsl import Q
from elasticsearch_dsl.query import Bool
from flask import request
from flask_login import current_user
from invenio_records_rest.query import es_search_factory
from oarepo_communities.api import OARepoCommunity
from oarepo_communities.constants import STATE_PUBLISHED, STATE_APPROVED
from oarepo_communities.proxies import current_oarepo_communities
from oarepo_communities.search import CommunitySearch

from .permissions import (
    AUTHENTICATED_PERMISSION,
    COMMUNITY_MEMBER_PERMISSION,
    COMMUNITY_CURATOR_PERMISSION
)


class NRRecordsSearch(CommunitySearch):
    LIST_SOURCE_FIELDS = []
    HIGHLIGHT_FIELDS = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._source = self._source = type(self).LIST_SOURCE_FIELDS
        for k, v in type(self).HIGHLIGHT_FIELDS.items():
            self._highlight[k] = v or {}

    class ActualMeta:
        outer_class = None
        doc_types = ['_doc']

        @classproperty
        def default_anonymous_filter(cls):
            return Q('term', _administration__state=STATE_PUBLISHED)

        @classproperty
        def default_authenticated_filter(cls):
            return Q('terms', state=[STATE_PUBLISHED])

        @classmethod
        def default_filter_factory(cls, search=None, **kwargs):
            if not request.view_args.get('community_id'):
                if not AUTHENTICATED_PERMISSION.can():
                    return cls.outer_class.Meta.default_anonymous_filter

                roles = current_user.roles
                my_communities = []
                for role in roles:
                    try:
                        my_communities.append(role.community.one().id)
                    except:
                        pass
                return Bool(should=[
                    cls.outer_class.Meta.default_authenticated_filter,
                    Q('terms', **{current_oarepo_communities.primary_community_field: my_communities}),
                    Q('terms', **{current_oarepo_communities.communities_field: my_communities})
                ], minimum_should_match=1)

            if not AUTHENTICATED_PERMISSION.can():
                # Anonymous sees published community records only
                return Bool(must=[
                    cls.outer_class.Meta.default_anonymous_filter,
                    CommunitySearch.community_filter()])

            if (
                    not COMMUNITY_MEMBER_PERMISSION(None).can() and
                    not COMMUNITY_CURATOR_PERMISSION(None).can()
            ):
                # non-community members sees the same as anonymous
                return Bool(must=[
                    cls.outer_class.Meta.default_anonymous_filter,
                    CommunitySearch.community_filter()])

            # member or curator
            if COMMUNITY_CURATOR_PERMISSION(None).can():
                # Curators can see all community records
                return CommunitySearch.community_filter()

            # member sees authenticated results filtered by community
            q = Bool(must=[
                CommunitySearch.community_filter(),
                cls.outer_class.Meta.default_authenticated_filter])
            return q

    @classproperty
    @functools.lru_cache(maxsize=1)
    def Meta(cls):
        return type(f'{cls.__name__}.Meta', (cls.ActualMeta,), {'outer_class': cls})


def community_search_factory(list_resource, records_search, **kwargs):
    community_id = getattr(request, 'view_args', {}).get('community_id')

    endpoint = request.endpoint  # 'invenio_records_rest.draft-nresults-community_list'
    endpoint = endpoint.split('.')[1]
    endpoint = re.sub('_list$', '', endpoint)

    index_name = records_search._index

    query, params = es_search_factory(list_resource, records_search, **kwargs)
    if community_id:
        params = {
            **params,
            'community_id': community_id
        }
    return query, params
