import os

from flask import url_for
from invenio_records.api import Record
from oarepo_communities.converters import CommunityPIDValue
from oarepo_communities.proxies import current_oarepo_communities
from oarepo_communities.record import CommunityRecordMixin
from oarepo_records_draft.record import InvalidRecordAllowedMixin, DraftRecordMixin
from oarepo_references.mixins import ReferenceEnabledRecordMixin
from oarepo_validate import SchemaKeepingRecordMixin, MarshmallowValidatedRecordMixin

from nr_nresults.constants import NRESULTS_ALLOWED_SCHEMAS, NRESULTS_PREFERRED_SCHEMA, published_index_name, \
    draft_index_name, all_nresults_index_name
from nr_nresults.marshmallow import NResultsMetadataSchemaV1


class NResultBaseRecord(SchemaKeepingRecordMixin,
                        MarshmallowValidatedRecordMixin,
                        ReferenceEnabledRecordMixin,
                        CommunityRecordMixin,
                        Record,
                        ):
    ALLOWED_SCHEMAS = NRESULTS_ALLOWED_SCHEMAS
    PREFERRED_SCHEMA = NRESULTS_PREFERRED_SCHEMA
    MARSHMALLOW_SCHEMA = NResultsMetadataSchemaV1


class PublishedNResultRecord(InvalidRecordAllowedMixin, NResultBaseRecord):
    index_name = published_index_name

    @property
    def canonical_url(self):
        return url_for('invenio_records_rest.nresults-community_item',
                       pid_value=CommunityPIDValue(
                           self['control_number'],
                           current_oarepo_communities.get_primary_community_field(self)),
                       _external=True)


class DraftNResultRecord(DraftRecordMixin, NResultBaseRecord):
    index_name = draft_index_name

    @property
    def canonical_url(self):
        return url_for('invenio_records_rest.draft-nresults-community_item',
                       pid_value=CommunityPIDValue(
                           self['control_number'],
                           current_oarepo_communities.get_primary_community_field(self)),
                       _external=True)


class AllNResultRecord(SchemaKeepingRecordMixin, CommunityRecordMixin, Record):
    ALLOWED_SCHEMAS = NRESULTS_ALLOWED_SCHEMAS
    PREFERRED_SCHEMA = NRESULTS_PREFERRED_SCHEMA
    index_name = all_nresults_index_name

    @property
    def canonical_url(self):
        if not self.get('oarepo:draft'):
            endpoint = 'invenio_records_rest.nresults-community_item'
        else:
            endpoint = 'invenio_records_rest.draft-nresults-community_item'

        return url_for(endpoint,
                       pid_value=CommunityPIDValue(
                           self['control_number'],
                           current_oarepo_communities.get_primary_community_field(self)),
                       _external=True)
