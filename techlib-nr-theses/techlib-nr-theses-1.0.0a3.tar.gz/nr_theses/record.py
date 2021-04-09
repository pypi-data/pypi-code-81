import os

from flask import url_for
from invenio_records.api import Record
from oarepo_communities.converters import CommunityPIDValue
from oarepo_communities.proxies import current_oarepo_communities
from oarepo_communities.record import CommunityRecordMixin
from oarepo_fsm.mixins import FSMMixin
from oarepo_records_draft.record import InvalidRecordAllowedMixin, DraftRecordMixin
from oarepo_references.mixins import ReferenceEnabledRecordMixin
from oarepo_validate import SchemaKeepingRecordMixin, MarshmallowValidatedRecordMixin

from .constants import THESES_ALLOWED_SCHEMAS, THESES_PREFERRED_SCHEMA
from .marshmallow import ThesisMetadataSchemaV2

published_index_name = 'nr_theses-nr-theses-v1.0.0'
draft_index_name = 'draft-nr_theses-nr-theses-v1.0.0'
all_index_name = 'nr-all'

prefixed_published_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX',
                                               '') + published_index_name
prefixed_draft_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX', '') + draft_index_name
prefixed_all_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX', '') + all_index_name


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
        return url_for('invenio_records_rest.theses_item',
                       pid_value=CommunityPIDValue(
                           self['control_number'],
                           current_oarepo_communities.get_primary_community_field(self)),
                       _external=True)


class DraftThesisRecord(DraftRecordMixin, ThesisBaseRecord):
    index_name = draft_index_name

    @property
    def canonical_url(self):
        return url_for('invenio_records_rest.draft-theses_item',
                       pid_value=CommunityPIDValue(
                           self['control_number'],
                           current_oarepo_communities.get_primary_community_field(self)),
                       _external=True)
