from invenio_search import RecordsSearch
from nr_common.search import NRRecordsSearch


class NResultsRecordsSearch(NRRecordsSearch):
    LIST_SOURCE_FIELDS = [
        'control_number', 'oarepo:validity.valid', 'oarepo:draft', 'title', 'dateIssued',
        'creator', 'resourceType', 'contributor', 'keywords', 'subject', 'abstract',
        'state',
        '_administration.primaryCommunity',
        '_administration.communities',
        '$schema'
    ]
    HIGHLIGHT_FIELDS = {
        'title.cs': None,
        'title._': None,
        'title.en': None
    }
