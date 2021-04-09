import os

EVENTS_ALLOWED_SCHEMAS = ['nr_events/nr-events-v1.0.0.json']
EVENTS_PREFERRED_SCHEMA = 'nr_events/nr-events-v1.0.0.json'

DRAFT_EVENT_PID_TYPE = 'dnrevt'
DRAFT_EVENT_RECORD = 'nr_events.record:DraftEventRecord'

PUBLISHED_EVENT_PID_TYPE = 'nrevt'
PUBLISHED_EVENT_RECORD = 'nr_events.record:PublishedEventRecord'

ALL_EVENTS_PID_TYPE = 'anrevt'
ALL_EVENTS_RECORD_CLASS = 'nr_events.record:AllEventRecord'

published_index_name = 'nr_events-nr-events-v1.0.0'
draft_index_name = 'draft-nr_events-nr-events-v1.0.0'
all_events_index_name = 'nr-all-events'

prefixed_published_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX',
                                               '') + published_index_name
prefixed_draft_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX', '') + draft_index_name
prefixed_all_events_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX', '') + all_events_index_name
