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

from oarepo_rdm_records.marshmallow.resource import ResourceTypeSchema
from oarepo_rdm_records.marshmallow.utils import _not_blank


class IdentifierSchema(Schema):
    """Identifier schema.

    NOTE: Equivalent to DataCite's alternate identifier.
    """

    identifier = SanitizedUnicode(
        required=True, validate=_not_blank(_('Identifier cannot be blank.')))
    scheme = SanitizedUnicode(
        required=True, validate=_not_blank(_('Scheme cannot be blank.')))


class RelatedIdentifierSchema(Schema):
    """Related identifier schema."""

    RELATIONS = [
        "iscitedby",
        "cites",
        "issupplementto",
        "issupplementedby",
        "iscontinuedby",
        "continues",
        "isdescribedby",
        "describes",
        "hasmetadata",
        "ismetadatafor",
        "hasversion",
        "isversionof",
        "isnewversionof",
        "ispreviousversionof",
        "ispartof",
        "haspart",
        "isreferencedby",
        "references",
        "isdocumentedby",
        "documents",
        "iscompiledby",
        "compiles",
        "isvariantformof",
        "isoriginalformof",
        "isidenticalto",
        "isreviewedby",
        "reviews",
        "isderivedfrom",
        "issourceof",
        "isrequiredby",
        "requires",
        "isobsoletedby",
        "obsoletes"
    ]

    SCHEMES = [
        "ark",
        "arxiv",
        "bibcode",
        "doi",
        "ean13",
        "eissn",
        "handle",
        "igsn",
        "isbn",
        "issn",
        "istc",
        "lissn",
        "lsid",
        "pmid",
        "purl",
        "upc",
        "url",
        "urn",
        "w3id"
    ]

    identifier = SanitizedUnicode(
        required=True,
        validate=_not_blank(_('Identifier cannot be blank.'))
    )
    scheme = SanitizedUnicode(required=True, validate=validate.OneOf(
        choices=SCHEMES,
        error=_('Invalid related identifier scheme. ' +
                '{input} not one of {choices}.')
    ))
    relation_type = SanitizedUnicode(required=True, validate=validate.OneOf(
        choices=RELATIONS,
        error=_('Invalid relation type. {input} not one of {choices}.')
    ))
    resource_type = fields.Nested(ResourceTypeSchema)
