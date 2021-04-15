# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RDM record schemas."""

from flask_babelex import lazy_gettext as _
from marshmallow import Schema, fields, validate
from marshmallow_utils.fields import EDTFDateString


class DateSchema(Schema):
    """Schema for date intervals."""

    DATE_TYPES = [
        "accepted",
        "available",
        "copyrighted",
        "collected",
        "created",
        "issued",
        "submitted",
        "updated",
        "valid",
        "withdrawn",
        "other"
    ]

    date = EDTFDateString(required=True)
    type = fields.Str(required=True, validate=validate.OneOf(
        choices=DATE_TYPES,
        error=_('Invalid date type. {input} not one of {choices}.')
    ))
    description = fields.Str()
