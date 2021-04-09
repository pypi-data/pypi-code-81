import os

COMMON_ALLOWED_SCHEMAS = ['nr_common/nr-common-v1.0.0.json']
COMMON_PREFERRED_SCHEMA = 'nr_common/nr-common-v1.0.0.json'

DRAFT_COMMON_PID_TYPE = 'dnrcom'
DRAFT_COMMON_RECORD = 'nr_generic.record:DraftCommonRecord'

PUBLISHED_COMMON_PID_TYPE = 'nrcom'
PUBLISHED_COMMON_RECORD = 'nr_generic.record:PublishedCommonRecord'

ALL_COMMON_PID_TYPE = 'anrcom'
ALL_COMMON_RECORD_CLASS = 'nr_generic.record:AllCommonRecord'

published_index_name = 'nr_common-nr-common-v1.0.0'
draft_index_name = 'draft-nr_common-nr-common-v1.0.0'
all_common_index_name = 'nr-all-common'

prefixed_published_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX',
                                               '') + published_index_name
prefixed_draft_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX', '') + draft_index_name
prefixed_all_common_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX', '') + all_common_index_name
