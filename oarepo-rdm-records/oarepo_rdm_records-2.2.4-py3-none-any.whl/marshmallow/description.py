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
from marshmallow import validate
from marshmallow_utils.fields import SanitizedUnicode
from oarepo_multilingual.marshmallow import MultilingualStringV2


class DescriptionSchema(StrictKeysMixin):
    """Schema for the additional descriptions."""

    DESCRIPTION_TYPES = [
        "abstract",
        "methods",
        "seriesinformation",
        "tableofcontents",
        "technicalinfo",
        "other"
    ]
    description = MultilingualStringV2(required=True)
    type = SanitizedUnicode(required=True,
                            default=DESCRIPTION_TYPES[0],
                            validate=validate.OneOf(
                                choices=DESCRIPTION_TYPES,
                                error=_('Invalid description type. {input} not one of {choices}.')
                            ))
