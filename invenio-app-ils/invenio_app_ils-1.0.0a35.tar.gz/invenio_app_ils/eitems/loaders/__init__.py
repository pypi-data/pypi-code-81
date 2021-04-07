# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# invenio-app-ils is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""ILS eitems loaders."""

from invenio_app_ils.records.loaders import ils_marshmallow_loader

from .jsonschemas.eitems import EItemSchemaV1

eitem_loader = ils_marshmallow_loader(EItemSchemaV1)
