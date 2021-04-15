# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RDM record schemas."""

from flask_babelex import lazy_gettext as _
from marshmallow import Schema
from marshmallow_utils.fields import SanitizedUnicode

from oarepo_rdm_records.marshmallow.utils import _is_uri


class RightsSchema(Schema):
    """License schema."""

    rights = SanitizedUnicode(required=True)
    uri = SanitizedUnicode(
        validate=_is_uri,
        error=_('Wrong URI format. Should follow RFC 3986.')
    )
    identifier = SanitizedUnicode()
    scheme = SanitizedUnicode()
