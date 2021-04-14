# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# My site is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""JSON Schemas."""
import arrow
from invenio_records_rest.schemas.fields.datetime import DateString
from marshmallow import fields, validates, ValidationError
from nr_common.marshmallow import CommonMetadataSchemaV2
from nr_common.marshmallow.subschemas import TitledMixin, InstitutionsMixin
from oarepo_taxonomies.marshmallow import TaxonomyField

from nr_theses.marshmallow.subschemas import StudyFieldMixin


class ThesisMetadataSchemaV2(CommonMetadataSchemaV2):
    dateDefended = DateString(required=True)
    defended = fields.Boolean(required=True)
    degreeGrantor = TaxonomyField(mixins=[TitledMixin, InstitutionsMixin], required=True)
    studyField = TaxonomyField(name="studyField", mixins=[TitledMixin, StudyFieldMixin])

    @validates("dateDefended")
    def validate_date_range(self, value):
        date = arrow.get(value)
        min_ = arrow.get("1700-01-01")
        current_date = arrow.get()
        if date > current_date:
            raise ValidationError("Date cannot be in the future")
        if date < min_:
            raise ValidationError("Records older than from 1700 is not supported")
