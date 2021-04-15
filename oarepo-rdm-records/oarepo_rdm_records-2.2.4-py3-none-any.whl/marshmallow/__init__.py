# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET Prague.
#
# CIS theses repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Schemas for marshmallow."""

from .access import AccessSchema
from .dataset import DataSetMetadataSchemaV1
from .dates import DateSchema
from .description import DescriptionSchema
from .identifier import IdentifierSchema, RelatedIdentifierSchema
from .language import LanguageSchema
from .person import (
    AffiliationSchema,
    ContributorSchema,
    CreatibutorSchema,
    CreatorSchema,
)
from .pids import PIDSchema
from .reference import ReferenceSchema
from .resource import ResourceTypeSchema
from .rights import RightsSchema

__all__ = ('DataSetMetadataSchemaV1', 'AccessSchema',
           'DateSchema', 'DescriptionSchema', 'IdentifierSchema',
           'RelatedIdentifierSchema', 'LanguageSchema', 'AffiliationSchema',
           'ContributorSchema', 'CreatorSchema', 'CreatibutorSchema',
           'PIDSchema', 'ReferenceSchema', 'ResourceTypeSchema', 'RightsSchema')
