import os

from flask import url_for
from invenio_records.api import Record
from nr_common.marshmallow import CommonMetadataSchemaV2
from oarepo_communities.converters import CommunityPIDValue
from oarepo_communities.proxies import current_oarepo_communities
from oarepo_communities.record import CommunityRecordMixin
from oarepo_records_draft.record import InvalidRecordAllowedMixin, DraftRecordMixin
from oarepo_references.mixins import ReferenceEnabledRecordMixin
from oarepo_validate import SchemaKeepingRecordMixin, MarshmallowValidatedRecordMixin

from .constants import COMMON_ALLOWED_SCHEMAS, COMMON_PREFERRED_SCHEMA, published_index_name, draft_index_name, \
    all_common_index_name


class CommonBaseRecord(SchemaKeepingRecordMixin,
                       MarshmallowValidatedRecordMixin,
                       ReferenceEnabledRecordMixin,
                       CommunityRecordMixin,
                       Record,
                       ):
    ALLOWED_SCHEMAS = COMMON_ALLOWED_SCHEMAS
    PREFERRED_SCHEMA = COMMON_PREFERRED_SCHEMA
    MARSHMALLOW_SCHEMA = CommonMetadataSchemaV2


class PublishedCommonRecord(InvalidRecordAllowedMixin, CommonBaseRecord):
    index_name = published_index_name

    @property
    def canonical_url(self):
        return url_for('invenio_records_rest.common-community_item',
                       pid_value=CommunityPIDValue(
                           self['control_number'],
                           current_oarepo_communities.get_primary_community_field(self)),
                       _external=True)


class DraftCommonRecord(DraftRecordMixin, CommonBaseRecord):
    index_name = draft_index_name

    @property
    def canonical_url(self):
        return url_for('invenio_records_rest.draft-common-community_item',
                       pid_value=CommunityPIDValue(
                           self['control_number'],
                           current_oarepo_communities.get_primary_community_field(self)),
                       _external=True)


class AllCommonRecord(SchemaKeepingRecordMixin, CommunityRecordMixin, Record):
    ALLOWED_SCHEMAS = COMMON_ALLOWED_SCHEMAS
    PREFERRED_SCHEMA = COMMON_PREFERRED_SCHEMA
    index_name = all_common_index_name
    # TODO: better canonical url based on if the class is published or not
