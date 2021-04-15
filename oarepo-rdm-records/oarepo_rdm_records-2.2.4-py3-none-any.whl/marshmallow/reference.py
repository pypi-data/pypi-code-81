# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RDM record schemas."""

from urllib import parse

from flask_babelex import lazy_gettext as _
from marshmallow import (
    EXCLUDE,
    INCLUDE,
    Schema,
    ValidationError,
    fields,
    validate,
    validates_schema,
)
from marshmallow_utils.fields import EDTFDateString, ISOLangString, SanitizedUnicode
from marshmallow_utils.schemas import GeometryObjectSchema


class ReferenceSchema(Schema):
    """Reference schema."""

    SCHEMES = [
        "isni",
        "grid",
        "crossreffunderid",
        "other"
    ]
    reference = SanitizedUnicode(required=True)
    identifier = SanitizedUnicode()
    scheme = SanitizedUnicode(validate=validate.OneOf(
        choices=SCHEMES,
        error=_('Invalid reference scheme. {input} not one of {choices}.')
    ))
