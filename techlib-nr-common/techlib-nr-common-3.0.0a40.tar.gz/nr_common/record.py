import os

from flask import url_for
from invenio_records.api import Record
from oarepo_communities.record import CommunityRecordMixin
from oarepo_fsm.mixins import FSMMixin
from oarepo_records_draft.record import InvalidRecordAllowedMixin, DraftRecordMixin
from oarepo_references.mixins import ReferenceEnabledRecordMixin
from oarepo_validate import SchemaKeepingRecordMixin, MarshmallowValidatedRecordMixin

from .constants import COMMON_ALLOWED_SCHEMAS, COMMON_PREFERRED_SCHEMA
from .marshmallow import CommonMetadataSchemaV2

published_index_name = 'nr_common-nr-common-v1.0.0'
draft_index_name = 'draft-nr_common-nr-common-v1.0.0'
all_index_name = 'nr-all'

prefixed_published_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX',
                                               '') + published_index_name
prefixed_draft_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX', '') + draft_index_name
prefixed_all_index_name = os.environ.get('INVENIO_SEARCH_INDEX_PREFIX', '') + all_index_name


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
        return url_for('invenio_records_rest.common_item',
                       pid_value=self['control_number'], _external=True)


class DraftCommonRecord(DraftRecordMixin, CommonBaseRecord):
    index_name = draft_index_name

    @property
    def canonical_url(self):
        return url_for('invenio_records_rest.draft-common_item',
                       pid_value=self['control_number'], _external=True)
