# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RDM record schemas."""
from invenio_records_rest.schemas import StrictKeysMixin
from marshmallow import EXCLUDE
from marshmallow_utils.fields import SanitizedUnicode
from oarepo_multilingual.marshmallow import validate_iso639_2


class LanguageSchema(StrictKeysMixin):
    """Language schema."""

    class Meta:
        """Meta class to discard unknown fields."""

        unknown = EXCLUDE

    code = SanitizedUnicode(required=True, validate=validate_iso639_2)
