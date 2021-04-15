# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET
#
# CIS theses repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marshmallow utility functions."""
from urllib import parse

import pycountry
from flask import current_app
from flask_babelex import lazy_gettext as _
from invenio_rest.serializer import BaseSchema
from marshmallow import ValidationError, fields, validate
from marshmallow.fields import Nested
from marshmallow.schema import SchemaMeta
from six.moves.urllib.parse import quote


def _no_duplicates(value_list):
    str_list = [str(value) for value in value_list]
    return len(value_list) == len(set(str_list))


def _not_blank(error_msg):
    """Return a non-blank validation rule with custom error message."""
    return validate.Length(min=1, error=error_msg)


def _is_uri(uri):
    try:
        parse.urlparse(uri)
        return True
    except AttributeError:
        return False


def validate_iso639_3(value):
    """Validate that language is ISO 639-3 value."""
    if not pycountry.languages.get(alpha_3=value):
        raise ValidationError(
            _('Language must be a lower-cased 3-letter ISO 639-3 string.'),
            field_name=['language']
        )


# TODO: Revist this links list.
# Ported from zenodo/modules/records/serializers/schemas/common.py#64

URLS = {
    'badge': '{base}/badge/doi/{doi}.svg',
    'bucket': '{base}/files/{bucket}',
    'funder': '{base}/funders/{id}',
    'grant': '{base}/grants/{id}',
    'object': '{base}/files/{bucket}/{key}',
    'deposit_html': '{base}/deposit/{id}',
    'deposit': '{base}/deposit/depositions/{id}',
    'record_html': '{base}/record/{id}',
    'record_file': '{base}/record/{id}/files/{filename}',
    'record': '{base}/records/{id}',
    'thumbnail': '{base}{path}',
    'thumbs': '{base}/record/{id}/thumb{size}',
    'community': '{base}/communities/{id}',
    'community_inclusion_request':
        '{base}/communities/{id}/requests/inclusion/{request_id}',
    'community_inclusion_request_action':
        '{base}/communities/{id}/requests/inclusion/{request_id}/{action}',
}


def link_for(base, tpl, **kwargs):
    """Create a link using specific template."""
    tpl = URLS.get(tpl)
    for k in ['key', ]:
        if k in kwargs:
            kwargs[k] = quote(kwargs[k].encode('utf8'))
    return tpl.format(base=base, **kwargs)


def api_link_for(tpl, **kwargs):
    """Create an API link using specific template."""
    is_api_app = 'invenio-deposit-rest' in current_app.extensions

    base = '{}/api'
    if current_app.testing and is_api_app:
        base = '{}'

    return link_for(
        base.format(current_app.config['THEME_SITEURL']), tpl, **kwargs)


def dump_empty(schema_or_field):
    """Return a full json-compatible dict with empty values.

    NOTE: This is only needed because the frontend needs it.
          This might change soon.
    """
    if isinstance(schema_or_field, (BaseSchema,)):
        schema = schema_or_field
        return {k: dump_empty(v) for (k, v) in schema.fields.items()}
    if isinstance(schema_or_field, SchemaMeta):
        # NOTE: Nested fields can pass a Schema class (SchemaMeta)
        #       or a Schema instance.
        #       Schema classes need to be instantiated to get .fields
        schema = schema_or_field()
        return {k: dump_empty(v) for (k, v) in schema.fields.items()}
    if isinstance(schema_or_field, fields.List):
        field = schema_or_field
        return [dump_empty(field.inner)]
    if isinstance(schema_or_field, Nested):
        field = schema_or_field
        return dump_empty(field.nested)

    return None
