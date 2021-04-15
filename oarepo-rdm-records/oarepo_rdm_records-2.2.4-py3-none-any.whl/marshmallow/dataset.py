# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RDM record schemas."""
from flask_babelex import lazy_gettext as _
from invenio_records_rest.schemas import StrictKeysMixin
from marshmallow import EXCLUDE, fields, validate
from marshmallow.fields import Nested
from marshmallow_utils.fields import EDTFDateString, SanitizedUnicode
from oarepo_invenio_model.marshmallow import (
    InvenioRecordMetadataFilesMixin,
    InvenioRecordMetadataSchemaV1Mixin,
)
from oarepo_multilingual.marshmallow import MultilingualStringV2

from oarepo_rdm_records.marshmallow import AccessSchema
from oarepo_rdm_records.marshmallow.dates import DateSchema
from oarepo_rdm_records.marshmallow.description import DescriptionSchema
from oarepo_rdm_records.marshmallow.identifier import (
    IdentifierSchema,
    RelatedIdentifierSchema,
)
from oarepo_rdm_records.marshmallow.language import LanguageSchema
from oarepo_rdm_records.marshmallow.person import ContributorSchema, CreatorSchema
from oarepo_rdm_records.marshmallow.reference import ReferenceSchema
from oarepo_rdm_records.marshmallow.resource import ResourceTypeSchema
from oarepo_rdm_records.marshmallow.rights import RightsSchema
from oarepo_rdm_records.marshmallow.utils import _no_duplicates


class DataSetMetadataSchemaV1(InvenioRecordMetadataFilesMixin,
                              InvenioRecordMetadataSchemaV1Mixin,
                              StrictKeysMixin):
    """DataSet reord schema."""

    class Meta:
        """Meta class."""

        unknown = EXCLUDE

    # Administrative fields
    _access = Nested(AccessSchema, required=False)
    _owners = fields.List(fields.Integer, validate=validate.Length(min=1),
                          required=True)
    _created_by = fields.Integer(required=True)
    _default_preview = SanitizedUnicode()

    # Metadata fields
    resource_type = fields.Nested(ResourceTypeSchema, required=True)
    identifiers = fields.List(fields.Nested(IdentifierSchema))
    publication_date = EDTFDateString(required=True)
    titles = fields.List(MultilingualStringV2(), required=True)
    creators = fields.List(fields.Nested(CreatorSchema), required=True)
    additional_titles = fields.List(MultilingualStringV2())
    abstract = fields.Nested(DescriptionSchema)
    version = SanitizedUnicode()
    language = fields.Nested(LanguageSchema)
    keywords = fields.List(SanitizedUnicode)
    additional_descriptions = fields.List(fields.Nested(DescriptionSchema))
    rights = fields.List(fields.Nested(RightsSchema))
    related_identifiers = fields.List(
        fields.Nested(RelatedIdentifierSchema),
        validate=_no_duplicates,
        error=_('Invalid related identifiers cannot contain duplicates.')
    )
    contributors = fields.List(fields.Nested(ContributorSchema))
    references = fields.List(fields.Nested(ReferenceSchema))
    dates = fields.List(fields.Nested(DateSchema))
