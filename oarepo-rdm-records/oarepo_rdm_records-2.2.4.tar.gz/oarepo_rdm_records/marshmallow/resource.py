# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RDM record schemas."""
from invenio_records_rest.schemas import StrictKeysMixin
from marshmallow import fields


class ResourceTypeSchema(StrictKeysMixin):
    """Resource type schema."""

    type = fields.Str(required=True)
    subtype = fields.Str()
