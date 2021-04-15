# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RDM record schemas."""

import idutils
from flask_babelex import lazy_gettext as _
from invenio_records_rest.schemas import StrictKeysMixin
from marshmallow import (
    ValidationError,
    fields,
    post_load,
    validate,
    validates,
    validates_schema,
)
from marshmallow_utils.fields import SanitizedUnicode


class AffiliationSchema(StrictKeysMixin):
    """Affiliation of a creator/contributor."""

    name = SanitizedUnicode(required=True)
    identifiers = fields.Dict()

    @validates("identifiers")
    def validate_identifiers(self, value):
        """Validate well-formed identifiers are passed."""
        if len(value) == 0:
            raise ValidationError(_("Invalid identifier."))

        for identifier in value.keys():
            validator = getattr(idutils, 'is_' + identifier, None)
            # NOTE: identifier key cannot be empty string
            if not identifier or (validator and
                                  not validator(value.get(identifier))):
                raise ValidationError(_(f"Invalid identifier ({identifier})."))


class CreatibutorSchema(StrictKeysMixin):
    """Creator/Contributor schema."""

    NAMES = [
        "organizational",
        "personal"
    ]

    type = SanitizedUnicode(
        required=True,
        validate=validate.OneOf(
            choices=NAMES,
            error=_(f'Invalid value. Choose one of {NAMES}.')
        ),
        error_messages={
            # NOTE: [] needed to mirror above error message
            "required": [_(f'Invalid value. Choose one of {NAMES}.')]
        }
    )
    name = SanitizedUnicode()
    given_name = SanitizedUnicode()
    family_name = SanitizedUnicode()
    identifiers = fields.Dict()
    affiliations = fields.List(fields.Nested(AffiliationSchema))

    @validates("identifiers")
    def validate_identifiers(self, value):
        """Validate well-formed identifiers are passed."""
        schemes = ['orcid', 'ror']

        if any(scheme not in schemes for scheme in value.keys()):
            raise ValidationError(
                [_(f"Invalid value. Choose one of {schemes}.")]
            )

        if 'orcid' in value:
            if not idutils.is_orcid(value.get('orcid')):
                raise ValidationError({'orcid': [_("Invalid value.")]})

        if 'ror' in value:
            if not idutils.is_ror(value.get('ror')):
                raise ValidationError({'ror': [_("Invalid value.")]})

    @validates_schema
    def validate_type_identifiers(self, data, **kwargs):
        """Validate identifier based on type."""
        if data['type'] == "personal":
            person_identifiers = ['orcid']
            identifiers = data.get('identifiers', {}).keys()
            if any([i not in person_identifiers for i in identifiers]):
                messages = [
                    _(f"Invalid value. Choose one of {person_identifiers}.")
                ]
                raise ValidationError({"identifiers": messages})

        elif data['type'] == "organizational":
            org_identifiers = ['ror']
            identifiers = data.get('identifiers', {}).keys()
            if any([i not in org_identifiers for i in identifiers]):
                messages = [
                    _(f"Invalid value. Choose one of {org_identifiers}.")
                ]
                raise ValidationError({"identifiers": messages})

    @validates_schema
    def validate_names(Self, data, **kwargs):
        """Validate names based on type."""
        if data['type'] == "personal":
            if not (data.get('given_name') or data.get('family_name')):
                messages = [_(f"One name must be filled.")]
                raise ValidationError({
                    "given_name": messages,
                    "family_name": messages
                })

        elif data['type'] == "organizational":
            if not data.get('name'):
                messages = [_('Name cannot be blank.')]
                raise ValidationError({"name": messages})

    @post_load
    def update_names(self, data, **kwargs):
        """Update names for organization / person.

        Fill name from given_name and family_name if person.
        Remove given_name and family_name if organization.
        """
        if data["type"] == "personal":
            names = [data.get("family_name"), data.get("given_name")]
            data["name"] = ", ".join([n for n in names if n])

        elif data['type'] == "organizational":
            if 'family_name' in data:
                del data['family_name']
            if 'given_name' in data:
                del data['given_name']

        return data


class CreatorSchema(CreatibutorSchema):
    """Creator schema."""

    role = SanitizedUnicode()


class ContributorSchema(CreatibutorSchema):
    """Contributor schema."""

    role = SanitizedUnicode(required=True)
