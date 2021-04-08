import functools

from boltons.typeutils import classproperty
from elasticsearch_dsl import Q
from elasticsearch_dsl.query import Bool
from oarepo_communities.constants import STATE_PUBLISHED, STATE_APPROVED
from oarepo_communities.search import CommunitySearch

from .permissions import (
    AUTHENTICATED_PERMISSION,
    COMMUNITY_MEMBER_PERMISSION,
    COMMUNITY_CURATOR_PERMISSION
)


class NRRecordsSearch(CommunitySearch):
    LIST_SOURCE_FIELDS = []
    HIGHLIGHT_FIELDS = {}

    only = None
    """one of ONLY_DRAFTS, ONLY_PUBLISHED"""

    ONLY_DRAFTS = 'drafts'
    ONLY_PUBLISHED = 'published'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._source = self._source = type(self).LIST_SOURCE_FIELDS
        for k, v in type(self).HIGHLIGHT_FIELDS:
            self._highlight[k] = v or {}

    class ActualMeta:
        outer_class = None
        doc_types = ['_doc']

        @classproperty
        def default_anonymous_filter(cls):
            if cls.outer_class.only == cls.outer_class.ONLY_DRAFTS:
                return Q('match_none')
            return Q('term', _administration__state=STATE_PUBLISHED)

        @classproperty
        def default_authenticated_filter(cls):
            if cls.outer_class.only == cls.outer_class.ONLY_DRAFTS:
                return Q('match_none')
            return Q('terms', state=[STATE_PUBLISHED])

        @classmethod
        def default_filter_factory(cls, search=None, **kwargs):
            if not AUTHENTICATED_PERMISSION.can() or not (
                    COMMUNITY_MEMBER_PERMISSION(None).can() or COMMUNITY_CURATOR_PERMISSION(None).can()):
                # Anonymous or non-community members sees published community records only
                return Bool(must=[
                    cls.outer_class.Meta.default_anonymous_filter,
                    CommunitySearch.community_filter()])
            else:
                if COMMUNITY_CURATOR_PERMISSION(None).can():
                    # Curators can see all community records
                    if cls.outer_class.only == cls.outer_class.ONLY_DRAFTS:
                        return Bool(
                            must=[
                                CommunitySearch.community_filter()],
                            must_not=[
                                Q('term', _administration__state=STATE_PUBLISHED),
                            ])
                    elif cls.outer_class.only == cls.outer_class.ONLY_PUBLISHED:
                        return Bool(must=[
                            Q('term', _administration__state=STATE_PUBLISHED),
                            CommunitySearch.community_filter()])
                    else:
                        return CommunitySearch.community_filter()

                q = Bool(must=[
                    CommunitySearch.community_filter(),
                    cls.outer_class.Meta.default_authenticated_filter])
            return q

    @classproperty
    @functools.lru_cache(maxsize=1)
    def Meta(cls):
        return type(f'{cls.__name__}.Meta', (cls.ActualMeta,), {'outer_class': cls})
