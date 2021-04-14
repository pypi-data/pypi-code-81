import os

THESES_ALLOWED_SCHEMAS = ['nr_theses/nr-theses-v1.0.0.json']
THESES_PREFERRED_SCHEMA = 'nr_theses/nr-theses-v1.0.0.json'

DRAFT_THESIS_PID_TYPE = 'dnrthe'
DRAFT_THESIS_RECORD = 'nr_theses.record:DraftThesisRecord'

PUBLISHED_THESIS_PID_TYPE = 'nrthe'
PUBLISHED_THESIS_RECORD = 'nr_theses.record:PublishedThesisRecord'

ALL_THESES_PID_TYPE = 'anrthe'
ALL_THESES_RECORD_CLASS = 'nr_theses.record:AllThesisRecord'

published_index_name = 'nr_theses-nr-theses-v1.0.0'
draft_index_name = 'draft-nr_theses-nr-theses-v1.0.0'
all_index_name = 'nr-all'
all_theses_index_name = 'nr-all-theses'

prefixed_published_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX',
                                               '') + published_index_name
prefixed_draft_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX', '') + draft_index_name
prefixed_all_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX', '') + all_index_name
prefixed_all_theses_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX', '') + 'nr-all-theses'
