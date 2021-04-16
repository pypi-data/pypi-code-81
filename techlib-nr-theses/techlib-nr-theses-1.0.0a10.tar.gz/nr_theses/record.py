from flask import url_for
from invenio_records.api import Record
from oarepo_communities.converters import CommunityPIDValue
from oarepo_communities.proxies import current_oarepo_communities
from oarepo_communities.record import CommunityRecordMixin
from oarepo_records_draft.record import InvalidRecordAllowedMixin, DraftRecordMixin
from oarepo_references.mixins import ReferenceEnabledRecordMixin
from oarepo_validate import SchemaKeepingRecordMixin, MarshmallowValidatedRecordMixin

from .constants import THESES_ALLOWED_SCHEMAS, THESES_PREFERRED_SCHEMA, published_index_name, draft_index_name, \
    all_theses_index_name
from .marshmallow import ThesisMetadataSchemaV2


class ThesisBaseRecord(SchemaKeepingRecordMixin,
                       MarshmallowValidatedRecordMixin,
                       ReferenceEnabledRecordMixin,
                       CommunityRecordMixin,
                       Record,
                       ):
    ALLOWED_SCHEMAS = THESES_ALLOWED_SCHEMAS
    PREFERRED_SCHEMA = THESES_PREFERRED_SCHEMA
    MARSHMALLOW_SCHEMA = ThesisMetadataSchemaV2


class PublishedThesisRecord(InvalidRecordAllowedMixin, ThesisBaseRecord):
    index_name = published_index_name

    @property
    def canonical_url(self):
        return url_for('invenio_records_rest.theses-community_item',
                       pid_value=CommunityPIDValue(
                           self['control_number'],
                           current_oarepo_communities.get_primary_community_field(self)),
                       _external=True)


class DraftThesisRecord(DraftRecordMixin, ThesisBaseRecord):
    index_name = draft_index_name

    @property
    def canonical_url(self):
        return url_for('invenio_records_rest.draft-theses-community_item',
                       pid_value=CommunityPIDValue(
                           self['control_number'],
                           current_oarepo_communities.get_primary_community_field(self)),
                       _external=True)


class AllThesisRecord(SchemaKeepingRecordMixin, CommunityRecordMixin, Record):
    ALLOWED_SCHEMAS = THESES_ALLOWED_SCHEMAS
    PREFERRED_SCHEMA = THESES_PREFERRED_SCHEMA
    index_name = all_theses_index_name
    # TODO: better canonical url based on if the class is published or not
