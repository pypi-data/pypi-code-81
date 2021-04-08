from elasticsearch_dsl import Q
from elasticsearch_dsl.query import Bool
from oarepo_communities.constants import STATE_PUBLISHED, STATE_APPROVED
from oarepo_communities.search import CommunitySearch

from .permissions import (
    AUTHENTICATED_PERMISSION,
    COMMUNITY_MEMBER_PERMISSION,
    COMMUNITY_CURATOR_PERMISSION
)


class ThesisRecordsSearch(CommunitySearch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._source = self._source = [
            'control_number', 'oarepo:validity.valid', 'oarepo:draft', 'title', 'dateIssued',
            'creator', 'resourceType', 'contributor', 'keywords', 'subject', 'abstract', 'state',
            '_administration.primaryCommunity',
            '_administration.communities',
        ]
        self._highlight['title.cs'] = {}
        self._highlight['title._'] = {}
        self._highlight['title.en'] = {}

    class Meta:
        doc_types = ['_doc']
        default_anonymous_filter = Q('term', _administration__state=STATE_PUBLISHED)
        default_authenticated_filter = Q('terms', state=[STATE_APPROVED, STATE_PUBLISHED])

        @staticmethod
        def default_filter_factory(search=None, **kwargs):
            if not AUTHENTICATED_PERMISSION.can() or not (COMMUNITY_MEMBER_PERMISSION(None).can() or COMMUNITY_CURATOR_PERMISSION(None).can()):
                # Anonymous or non-community members sees published community records only
                return Bool(must=[
                    ThesisRecordsSearch.Meta.default_anonymous_filter,
                    CommunitySearch.community_filter()])
            else:
                if COMMUNITY_CURATOR_PERMISSION(None).can():
                    # Curators can see all community records
                    return CommunitySearch.community_filter()

                # Community member sees both APPROVED and PUBLISHED community records only
                q = Bool(must=[
                    CommunitySearch.community_filter(),
                    ThesisRecordsSearch.Meta.default_authenticated_filter])
            return q
