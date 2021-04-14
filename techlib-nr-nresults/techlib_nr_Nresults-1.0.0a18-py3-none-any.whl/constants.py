import os

NRESULTS_ALLOWED_SCHEMAS = ['nr_nresults/nr-nresults-v1.0.0.json']
NRESULTS_PREFERRED_SCHEMA = 'nr_nresults/nr-nresults-v1.0.0.json'


DRAFT_NRESULT_PID_TYPE = 'dnrnrs'
DRAFT_NRESULT_RECORD = 'nr_nresults.record:DraftNResultRecord'

PUBLISHED_NRESULT_PID_TYPE = 'nrnrs'
PUBLISHED_NRESULT_RECORD = 'nr_nresults.record:PublishedNResultRecord'

ALL_NRESULTS_PID_TYPE = 'anrnrs'
ALL_NRESULTS_RECORD_CLASS = 'nr_nresults.record:AllNResultRecord'


published_index_name = 'nr_nresults-nr-nresults-v1.0.0'
draft_index_name = 'draft-nr_nresults-nr-nresults-v1.0.0'
all_nresults_index_name = 'nr-all-nresults'


prefixed_published_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX',
                                               '') + published_index_name
prefixed_draft_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX', '') + draft_index_name
prefixed_all_nresults_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX', '') + all_nresults_index_name
