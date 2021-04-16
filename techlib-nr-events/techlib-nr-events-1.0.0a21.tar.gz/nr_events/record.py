import os

from flask import url_for
from invenio_records.api import Record
from oarepo_communities.converters import CommunityPIDValue
from oarepo_communities.proxies import current_oarepo_communities
from oarepo_communities.record import CommunityRecordMixin
from oarepo_records_draft.record import InvalidRecordAllowedMixin, DraftRecordMixin
from oarepo_references.mixins import ReferenceEnabledRecordMixin
from oarepo_validate import SchemaKeepingRecordMixin, MarshmallowValidatedRecordMixin

from .constants import EVENTS_ALLOWED_SCHEMAS, EVENTS_PREFERRED_SCHEMA, published_index_name, draft_index_name, \
    all_events_index_name
from .marshmallow import EventsMetadataSchemaV1


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
        return url_for('invenio_records_rest.events-community_item',
                       pid_value=CommunityPIDValue(
                           self['control_number'],
                           current_oarepo_communities.get_primary_community_field(self)),
                       _external=True)


class DraftEventRecord(DraftRecordMixin, EventBaseRecord):
    index_name = draft_index_name

    @property
    def canonical_url(self):
        return url_for('invenio_records_rest.draft-events-community_item',
                       pid_value=CommunityPIDValue(
                           self['control_number'],
                           current_oarepo_communities.get_primary_community_field(self)),
                       _external=True)


class AllEventRecord(SchemaKeepingRecordMixin, CommunityRecordMixin, Record):
    ALLOWED_SCHEMAS = EVENTS_ALLOWED_SCHEMAS
    PREFERRED_SCHEMA = EVENTS_PREFERRED_SCHEMA
    index_name = all_events_index_name

    @property
    def canonical_url(self):
        if not self.get('oarepo:draft'):
            endpoint = 'invenio_records_rest.events-community_item'
        else:
            endpoint = 'invenio_records_rest.draft-events-community_item'

        return url_for(endpoint,
                       pid_value=CommunityPIDValue(
                           self['control_number'],
                           current_oarepo_communities.get_primary_community_field(self)),
                       _external=True)
