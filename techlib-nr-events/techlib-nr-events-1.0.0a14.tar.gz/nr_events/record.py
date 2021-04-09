import os

from flask import url_for
from invenio_records.api import Record
from oarepo_communities.record import CommunityRecordMixin
from oarepo_records_draft.record import InvalidRecordAllowedMixin, DraftRecordMixin
from oarepo_references.mixins import ReferenceEnabledRecordMixin
from oarepo_validate import SchemaKeepingRecordMixin, MarshmallowValidatedRecordMixin

from .constants import EVENTS_ALLOWED_SCHEMAS, EVENTS_PREFERRED_SCHEMA
from .marshmallow import EventsMetadataSchemaV1

published_index_name = 'nr_events-nr-events-v1.0.0'
draft_index_name = 'draft-nr_events-nr-events-v1.0.0'
all_index_name = 'nr-all'

prefixed_published_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX',
                                               '') + published_index_name
prefixed_draft_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX', '') + draft_index_name
prefixed_all_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX', '') + all_index_name


class EventBaseRecord(SchemaKeepingRecordMixin,
                      MarshmallowValidatedRecordMixin,
                      ReferenceEnabledRecordMixin,
                      CommunityRecordMixin,
                      Record,
                      ):
    ALLOWED_SCHEMAS = EVENTS_ALLOWED_SCHEMAS
    PREFERRED_SCHEMA = EVENTS_PREFERRED_SCHEMA
    MARSHMALLOW_SCHEMA = EventsMetadataSchemaV1


class PublishedEventRecord(InvalidRecordAllowedMixin, EventBaseRecord):
    index_name = published_index_name

    @property
    def canonical_url(self):
        return url_for('invenio_records_rest.events_item',
                       pid_value=self['control_number'], _external=True)


class DraftEventRecord(DraftRecordMixin, EventBaseRecord):
    index_name = draft_index_name

    @property
    def canonical_url(self):
        return url_for('invenio_records_rest.draft-events_item',
                       pid_value=self['control_number'], _external=True)
